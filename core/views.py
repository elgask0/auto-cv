# core/views.py

from openai import OpenAI
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, EducationForm, ExperienceForm
from .models import UserProfile, Education, Experience
from django.conf import settings
from .forms import GenerationForm
from .models import Generation
from django.http import HttpResponse
import subprocess
import tempfile
import os
import base64

import logging
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

import logging

logger = logging.getLogger(__name__)

@login_required
def generate_documents(request):
    if request.method == 'POST':
        form = GenerationForm(request.POST)
        if form.is_valid():
            job_description = form.cleaned_data['job_description']
            generate_cv = form.cleaned_data['generate_cv']
            generate_cover_letter = form.cleaned_data['generate_cover_letter']
            
            selected_generations = []
            if generate_cv:
                selected_generations.append('cv')
            if generate_cover_letter:
                selected_generations.append('cover_letter')
            
            if not selected_generations:
                form.add_error(None, "Please select at least one document to generate.")
                return render(request, 'core/generate_documents.html', {'form': form})
            
            generated_documents = []
            client = OpenAI(api_key=settings.OPENAI_API_KEY)  # Initialize OpenAI client
            
            for gen_type in selected_generations:
                # Prepare the prompt based on the type
                if gen_type == 'cv':
                    prompt = (
                        f"Generate a professional Curriculum Vitae in LaTeX format for the following individual based on the job description.\n\n"
                        f"Job Description:\n{job_description}\n\n"
                        f"User Information:\n"
                        f"Name: {request.user.userprofile.name}\n"
                        f"Phone: {request.user.userprofile.phone}\n"
                        f"LinkedIn: {request.user.userprofile.linkedin_link}\n"
                        f"Summary: {request.user.userprofile.summary}\n"
                        f"Skills: {request.user.userprofile.skills}\n"
                        f"Publications: {request.user.userprofile.publications}\n"
                        f"Projects: {request.user.userprofile.projects}\n"
                        f"Interests: {request.user.userprofile.interests}\n\n"
                        f"Please return the LaTeX code enclosed within a JSON object with the key \"latex_code\".\n"
                        f"Example:\n{{\n    \"latex_code\": \"Your LaTeX code here\"\n}}"
                    )
                elif gen_type == 'cover_letter':
                    prompt = (
                        f"Generate a professional Cover Letter in LaTeX format for the following individual based on the job description.\n\n"
                        f"Job Description:\n{job_description}\n\n"
                        f"User Information:\n"
                        f"Name: {request.user.userprofile.name}\n"
                        f"Phone: {request.user.userprofile.phone}\n"
                        f"LinkedIn: {request.user.userprofile.linkedin_link}\n"
                        f"Summary: {request.user.userprofile.summary}\n"
                        f"Skills: {request.user.userprofile.skills}\n"
                        f"Publications: {request.user.userprofile.publications}\n"
                        f"Projects: {request.user.userprofile.projects}\n"
                        f"Interests: {request.user.userprofile.interests}\n\n"
                        f"Please return the LaTeX code enclosed within a JSON object with the key \"latex_code\".\n"
                        f"Example:\n{{\n    \"latex_code\": \"Your LaTeX code here\"\n}}"
                    )
                
                try:
                    # Call the OpenAI API to generate the JSON output
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1000,
                        temperature=0.8
                    )
                    
                    # Extract the JSON output from the response
                    json_output = response.choices[0].message.content.strip()
                    
                    # Parse the JSON string into a Python dictionary
                    json_data = json.loads(json_output)
                    
                    # Save the generation to the database
                    generation = Generation.objects.create(
                        user=request.user,
                        job_description=job_description,
                        generation_type=gen_type,
                        json_output=json_data,
                    )
                    
                    generated_documents.append(generation)
                
                except json.JSONDecodeError as json_err:
                    form.add_error(None, f"JSON decode error for {gen_type}: {str(json_err)}")
                    return render(request, 'core/generate_documents.html', {'form': form})
                
                except Exception as e:
                    form.add_error(None, f"Error generating {gen_type}: {str(e)}")
                    return render(request, 'core/generate_documents.html', {'form': form})
            
            # Redirect to the list of generated documents after successful generation
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
    logger.debug(f"Rendering LaTeX for Generation ID: {generation_id}")
    generation = get_object_or_404(Generation, id=generation_id, user=request.user)
    
    latex_code = generation.json_output.get('latex_code', '')
    logger.debug(f"Retrieved LaTeX code (length: {len(latex_code)} characters).")
    
    if not latex_code:
        logger.error(f"No LaTeX code found for Generation ID: {generation_id}")
        return HttpResponse("No LaTeX code found for this document.", status=400)
    
    # Define the full path to pdflatex
    pdflatex_path = "/Library/TeX/texbin/pdflatex"
    
    # Check if pdflatex exists
    if not os.path.exists(pdflatex_path):
        logger.error("pdflatex executable not found.")
        return HttpResponse(
            "pdflatex executable not found. Please ensure that LaTeX is installed correctly.",
            status=500
        )
    
    # Render LaTeX to PDF using a temporary file
    with tempfile.TemporaryDirectory() as temp_dir:
        logger.debug(f"Created temporary directory at {temp_dir}")
        tex_file_path = os.path.join(temp_dir, 'document.tex')
        pdf_file_path = os.path.join(temp_dir, 'document.pdf')
        
        # Write LaTeX code to .tex file
        with open(tex_file_path, 'w') as tex_file:
            tex_file.write(latex_code)
        logger.debug(f"Wrote LaTeX code to {tex_file_path}")
        
        # Compile LaTeX to PDF using pdflatex
        try:
            logger.debug("Starting pdflatex subprocess.")
            result = subprocess.run(
                [pdflatex_path, '-interaction=nonstopmode', tex_file_path],
                cwd=temp_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30  # Add a timeout to prevent hanging indefinitely
            )
            logger.debug("pdflatex subprocess completed successfully.")
        except subprocess.TimeoutExpired:
            logger.error("pdflatex subprocess timed out.")
            return HttpResponse("LaTeX compilation timed out.", status=500)
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode('utf-8')
            logger.error(f"Error compiling LaTeX: {error_message}")
            return HttpResponse(f"Error compiling LaTeX: {error_message}", status=500)
        except Exception as e:
            logger.error(f"Unexpected error during LaTeX compilation: {str(e)}")
            return HttpResponse(f"Unexpected error during LaTeX compilation: {str(e)}", status=500)
        
        # Read the generated PDF
        if not os.path.exists(pdf_file_path):
            logger.error("PDF file was not created.")
            return HttpResponse("PDF file was not created.", status=500)
        
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        logger.debug("Read compiled PDF content.")
    
    # Encode PDF content to base64 for embedding in HTML
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    
    # Render the LaTeX code and PDF preview on the web
    return render(request, 'core/render_latex.html', {
        'latex_code': latex_code,
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