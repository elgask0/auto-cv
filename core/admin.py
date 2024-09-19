# core/admin.py

from django.contrib import admin
from .models import UserProfile, Education, Experience
from .models import Generation

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'phone', 'linkedin_link']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['education_level', 'university', 'profile']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'profile']

@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'generation_type', 'created_at')
    list_display_links = ('id', 'user')  # Makes 'id' and 'user' clickable
    readonly_fields = ('id', 'created_at')  # Optional: make 'id' and 'created_at' read-only
    fields = ('id', 'user', 'job_description', 'generation_type', 'json_output', 'created_at')
