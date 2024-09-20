# core/views.py
import shutil
from openai import OpenAI
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, EducationForm, ExperienceForm, GenerationForm
from .models import UserProfile, Education, Experience, Generation
from .prompts import generate_cv_prompt, generate_cover_letter_prompt
from .utils import (
    escape_latex_special_chars,
    format_user_experience,
    format_user_education,
    format_user_list_field,
    user_info_to_prompt_format,
    LatexOutput,  # Import the function schema,
    clean_latex
)
from .templates import cv_template, cover_letter_template
from django.conf import settings
from django.http import HttpResponse
import subprocess
import tempfile
import os
import base64
from pydantic import ValidationError
import logging

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize the OpenAI client with the API key from settings
client = OpenAI(api_key=settings.OPENAI_API_KEY)

@login_required
def view_profile(request):
    profile = request.user.userprofile
    educations = profile.educations.all()
    experiences = profile.experiences.all()
    return render(request, 'core/view_profile.html', {
        'profile': profile,
        'educations': educations,
        'experiences': experiences,
    })

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.profile = request.user.userprofile
            education.save()
            return redirect('view_profile')
    else:
        form = EducationForm()
    return render(request, 'core/add_education.html', {'form': form})

@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = request.user.userprofile
            experience.save()
            return redirect('view_profile')
    else:
        form = ExperienceForm()
    return render(request, 'core/add_experience.html', {'form': form})




@login_required
def generate_documents(request):
    if request.method == 'POST':
        form = GenerationForm(request.POST)
        if form.is_valid():
            job_description = form.cleaned_data['job_description']
            generate_cv = form.cleaned_data['generate_cv']
            generate_cover_letter = form.cleaned_data['generate_cover_letter']
            
            # Escape the job description
            escaped_job_description = escape_latex_special_chars(job_description)
            
            user_profile = request.user.userprofile

            # Retrieve educations and experiences
            educations = user_profile.educations.all()
            experiences = user_profile.experiences.all()

            # Prepare user info
            user_info = {
                'name': escape_latex_special_chars(user_profile.name),
                'email': escape_latex_special_chars(request.user.email),
                'phone': escape_latex_special_chars(user_profile.phone),
                'education': format_user_education(educations),
                'experience': format_user_experience(experiences),
                'skills': format_user_list_field(user_profile.skills),
                'interests': format_user_list_field(user_profile.interests),
                'projects': format_user_list_field(user_profile.projects),
                'publications': format_user_list_field(user_profile.publications),
            }

            # Convert user_info to a formatted string for the prompt
            user_info_str = user_info_to_prompt_format(user_info)

            selected_generations = []
            if generate_cv:
                selected_generations.append('cv')
            if generate_cover_letter:
                selected_generations.append('cover_letter')

            if not selected_generations:
                form.add_error(None, "Please select at least one document to generate.")
                return render(request, 'core/generate_documents.html', {'form': form})

            for gen_type in selected_generations:
                if gen_type == 'cv':
                    template = cv_template
                    prompt = generate_cv_prompt(user_info_str, escaped_job_description, template)
                elif gen_type == 'cover_letter':
                    template = cover_letter_template
                    prompt = generate_cover_letter_prompt(user_info_str, escaped_job_description, template)
                
                try:
                    response = client.beta.chat.completions.parse(
                        model="gpt-4o-2024-08-06",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant designed to output LaTeX code in a structured format."},
                            {"role": "user", "content": prompt}
                        ],
                        response_format=LatexOutput,
                        max_tokens=5000,
                        temperature=0.7
                    )
                    
                    # Extract the parsed response using the Pydantic model
                    latex_output = response.choices[0].message.parsed
                    
                    # Save the generation
                    Generation.objects.create(
                        user=request.user,
                        job_description=job_description,
                        generation_type=gen_type,
                        json_output=latex_output.dict(),  # Convert Pydantic model to dictionary
                    )
                except ValidationError as ve:
                    logger.error(f"Pydantic validation error for {gen_type}: {ve}")
                    form.add_error(None, f"Error validating JSON output for {gen_type}. Please try again.")
                    return render(request, 'core/generate_documents.html', {'form': form})
                except Exception as e:
                    logger.error(f"Error generating {gen_type}: {e}")
                    form.add_error(None, f"Error generating {gen_type}: {e}")
                    return render(request, 'core/generate_documents.html', {'form': form})
            
            return redirect('document_list')
    else:
        form = GenerationForm(initial={'generate_cv': True})
    
    return render(request, 'core/generate_documents.html', {'form': form})

@login_required
def document_list(request):
    generations = Generation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/document_list.html', {'generations': generations})

@login_required
def render_latex(request, generation_id):
    """
    Renders the LaTeX code from the Generation model into a PDF and returns it.

    This view retrieves LaTeX code stored as a JSON string in the Generation model,
    cleans and formats it appropriately, compiles it using pdflatex, and returns
    the resulting PDF to the user.

    Parameters:
    - request: The HTTP request object.
    - generation_id (int): The ID of the Generation object containing LaTeX code.

    Returns:
    - HttpResponse: A response containing the compiled PDF or an error message.
    """
    logger.debug(f"Rendering LaTeX for Generation ID: {generation_id}")

    # Step 1: Retrieve the Generation object
    generation = get_object_or_404(Generation, id=generation_id, user=request.user)

    # Step 2: Retrieve the LaTeX code from the JSON output
    latex_code_raw = generation.json_output.get('latex_code', '')
    logger.debug(f"Retrieved LaTeX code (length: {len(latex_code_raw)} characters).")

    if not latex_code_raw:
        logger.error(f"No LaTeX code found for Generation ID: {generation_id}")
        return HttpResponse("No LaTeX code found for this document.", status=400)

    # Step 3: Clean the LaTeX code
    try:
        latex_code_clean = clean_latex(latex_code_raw)
        logger.debug("Successfully cleaned LaTeX code.")
    except ValueError as ve:
        logger.error(f"LaTeX cleaning failed: {ve}")
        return HttpResponse(f"LaTeX cleaning failed: {ve}", status=400)
    except Exception as e:
        logger.error(f"Unexpected error during LaTeX cleaning: {e}")
        return HttpResponse(f"Unexpected error during LaTeX cleaning: {e}", status=500)

    # Step 4: Locate the pdflatex executable
    pdflatex_path = shutil.which('pdflatex')
    if not pdflatex_path:
        logger.error("pdflatex executable not found in PATH.")
        return HttpResponse(
            "pdflatex executable not found. Please ensure that LaTeX is installed correctly and that 'pdflatex' is in your system's PATH.",
            status=500
        )
    logger.debug(f"Using pdflatex at: {pdflatex_path}")

    # Step 5: Create a temporary directory for LaTeX compilation
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_file_path = os.path.join(temp_dir, 'document.tex')
        pdf_file_path = os.path.join(temp_dir, 'document.pdf')

        # Step 6: Write the cleaned LaTeX code to the .tex file
        try:
            with open(tex_file_path, 'w', encoding='utf-8') as tex_file:
                tex_file.write(latex_code_clean)
            logger.debug(f"Wrote cleaned LaTeX code to {tex_file_path}")
        except Exception as e:
            logger.error(f"Failed to write LaTeX code to file: {e}")
            return HttpResponse("Failed to write LaTeX code to file.", status=500)

        # Optional: Log the written LaTeX code for debugging
        try:
            with open(tex_file_path, 'r', encoding='utf-8') as tex_file:
                written_latex_code = tex_file.read()
                logger.debug(f"Written LaTeX code:\n{written_latex_code}")
        except Exception as e:
            logger.warning(f"Failed to read written LaTeX code for logging: {e}")

        # Step 7: Compile the LaTeX code using pdflatex
        try:
            logger.debug("Starting pdflatex subprocess.")
            result = subprocess.run(
                [pdflatex_path, '-interaction=nonstopmode', tex_file_path],
                cwd=temp_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60  # Increased timeout to handle longer compilations
            )

            # Capture the standard output and error for debugging
            stdout = result.stdout.decode('utf-8')
            stderr = result.stderr.decode('utf-8')
            logger.debug(f"pdflatex stdout:\n{stdout}")
            logger.debug(f"pdflatex stderr:\n{stderr}")

        except subprocess.TimeoutExpired:
            logger.error("pdflatex subprocess timed out.")
            return HttpResponse("LaTeX compilation timed out.", status=500)
        except subprocess.CalledProcessError as e:
            # Capture and log the error message from pdflatex
            error_message = e.stderr.decode('utf-8') if e.stderr else "No stderr captured."
            logger.error(f"Error compiling LaTeX: {error_message}")
            return HttpResponse(f"Error compiling LaTeX: {error_message}", status=500)
        except Exception as e:
            logger.error(f"Unexpected error during LaTeX compilation: {str(e)}")
            return HttpResponse(f"Unexpected error during LaTeX compilation: {str(e)}", status=500)

        # Step 8: Check if the PDF was created successfully
        if not os.path.exists(pdf_file_path):
            logger.error("PDF file was not created.")
            return HttpResponse("PDF file was not created.", status=500)

        # Step 9: Read the generated PDF content
        try:
            with open(pdf_file_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
            logger.debug("Read compiled PDF content.")
        except Exception as e:
            logger.error(f"Failed to read compiled PDF: {e}")
            return HttpResponse("Failed to read compiled PDF.", status=500)

    # Step 10: Encode PDF content to base64 for embedding in HTML
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

    # Step 11: Render the LaTeX code and PDF preview in the template
    return render(request, 'core/render_latex.html', {
        'latex_code': latex_code_clean,
        'pdf_content': pdf_base64,
        'generation': generation,
    })

@login_required
def download_pdf(request, generation_id):
    generation = get_object_or_404(Generation, id=generation_id, user=request.user)
    
    latex_code = generation.json_output.get('latex_code', '')
    
    # Generate PDF from LaTeX
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_file_path = os.path.join(temp_dir, 'document.tex')
        pdf_file_path = os.path.join(temp_dir, 'document.pdf')
        
        # Write LaTeX code to .tex file
        with open(tex_file_path, 'w') as tex_file:
            tex_file.write(latex_code)
        
        # Compile LaTeX to PDF using pdflatex
        try:
            subprocess.run(['pdflatex', tex_file_path], cwd=temp_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Error compiling LaTeX: {e.stderr.decode('utf-8')}")
        
        # Read the generated PDF
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
    
    # Create HTTP response for file download
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{generation.get_generation_type_display()}_{generation.id}.pdf"'
    return response