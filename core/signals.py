# core/signals.py

from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


@receiver(user_signed_up)
def populate_user_profile(request, user, **kwargs):
    """
    Populate UserProfile and User model with data from Google.
    """
    if user.socialaccount_set.exists():
        google_account = user.socialaccount_set.filter(provider="google").first()
        if google_account:
            extra_data = google_account.extra_data

            user.email = extra_data.get("email", "")
            user.first_name = extra_data.get("given_name", "")
            user.last_name = extra_data.get("family_name", "")
            user.save()

            # Ensure UserProfile exists
            UserProfile.objects.get_or_create(user=user)
