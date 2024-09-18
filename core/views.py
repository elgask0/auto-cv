# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, EducationForm, ExperienceForm
from .models import UserProfile, Education, Experience

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
