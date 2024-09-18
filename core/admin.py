# core/admin.py

from django.contrib import admin
from .models import UserProfile, Education, Experience

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'phone', 'linkedin_link']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['education_level', 'university', 'profile']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'profile']
