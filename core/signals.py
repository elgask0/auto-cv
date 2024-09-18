# core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.signals import user_signed_up
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, name=instance.get_full_name())

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(user_signed_up)
def populate_user_profile(request, user, **kwargs):
    """
    Populate UserProfile with data from Google OAuth.
    """
    if user.socialaccount_set.exists():
        google_account = user.socialaccount_set.filter(provider='google').first()
        if google_account:
            extra_data = google_account.extra_data

            user.userprofile.name = extra_data.get('name', '')
            user.userprofile.phone = extra_data.get('phone_number', '')
            user.userprofile.linkedin_link = extra_data.get('link', '')  # Adjust based on actual keys
            user.userprofile.summary = extra_data.get('about', '')  # Adjust based on actual keys
            user.userprofile.save()
