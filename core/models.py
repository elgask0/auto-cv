# core/models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_link = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Enter skills separated by commas or new lines.")
    publications = models.TextField(blank=True, help_text="Enter publications separated by commas or new lines.")
    projects = models.TextField(blank=True, help_text="Enter projects separated by commas or new lines.")
    interests = models.TextField(blank=True, help_text="Enter interests separated by commas or new lines.")

    def __str__(self):
        return self.name

class Education(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
    education_level = models.CharField(max_length=100)  # e.g., Bachelor, Master
    university = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # Optional for ongoing studies
    specialization = models.CharField(max_length=255, blank=True)
    thesis = models.CharField(max_length=255, blank=True)
    relevant_subjects = models.TextField(blank=True)

    def __str__(self):
        return f"{self.education_level} at {self.university}"

class Experience(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # Optional for current positions
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
