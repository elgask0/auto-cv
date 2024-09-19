# core/views.py

import openai
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
            
            selected_generations = []
            if generate_cv:
                selected_generations.append('cv')
            if generate_cover_letter:
                selected_generations.append('cover_letter')
            
            if not selected_generations:
                form.add_error(None, "Please select at least one document to generate.")
                return render(request, 'core/generate_documents.html', {'form': form})
            
            generated_documents = []
            for gen_type in selected_generations:
                # Prepare the prompt based on the type                
                prompt = f"""
                            Generate a professional {'Curriculum Vitae' if gen_type == 'cv' else 'Cover Letter'} in LaTeX format for the following individual based on the job description.

                            Job Description:
                            {job_description}

                            User Information:
                            Name: {request.user.userprofile.name}
                            Phone: {request.user.userprofile.phone}
                            LinkedIn: {request.user.userprofile.linkedin_link}
                            Summary: {request.user.userprofile.summary}
                            Skills: {request.user.userprofile.skills}
                            Publications: {request.user.userprofile.publications}
                            Projects: {request.user.userprofile.projects}
                            Interests: {request.user.userprofile.interests}

                            Please return the LaTeX code enclosed within a JSON object with the key "latex_code".
                            Example:
                            {{
                                "latex_code": "Your LaTeX code here"
                            }}
                            """

                # Call OpenAI API
                openai.api_key = settings.OPENAI_API_KEY
                try:
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        max_tokens=2000,
                        temperature=0.7,
                    )
                    
                    # Assume the response is JSON with LaTeX parts
                    # For consistency, we expect OpenAI to return JSON
                    # Example:
                    # {
                    #     "latex_code": "..."
                    # }
                    # So we need to parse it
                    response_text = response.choices[0].text.strip()
                    json_output = json.loads(response_text)
                    
                    # Save the generation to the database
                    generation = Generation.objects.create(
                        user=request.user,
                        job_description=job_description,
                        generation_type=gen_type,
                        json_output=json_output,
                    )
                    
                    generated_documents.append(generation)
                
                except Exception as e:
                    form.add_error(None, f"Error generating {gen_type}: {str(e)}")
                    return render(request, 'core/generate_documents.html', {'form': form})
            
            # Redirect to the list of generated documents or display them
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
    generation = get_object_or_404(Generation, id=generation_id, user=request.user)
    
    latex_code = generation.json_output.get('latex_code', '')
    
    # Render LaTeX to PDF using a temporary file
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
    
    # Render the LaTeX code on the web (as raw text or using a LaTeX renderer)
    # For simplicity, we'll display it as raw LaTeX code
    # To render it beautifully, consider integrating a LaTeX rendering library or converting to HTML
    
    return render(request, 'core/render_latex.html', {
        'latex_code': latex_code,
        'pdf_content': pdf_content,
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