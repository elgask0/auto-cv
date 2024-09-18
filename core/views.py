# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile

@login_required
def user_profile(request):
    # Attempt to get or create the UserProfile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home or another appropriate page
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'core/user_profile.html', {'form': form})

def home(request):
    return render(request, 'core/home.html')
