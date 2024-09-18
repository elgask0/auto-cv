# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home view
    path('profile/', views.user_profile, name='user_profile'),  # User profile view
    # Add other URL patterns as needed
]