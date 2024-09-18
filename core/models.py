# core/models.py

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
