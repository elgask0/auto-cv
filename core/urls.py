# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('add-education/', views.add_education, name='add_education'),
    path('add-experience/', views.add_experience, name='add_experience'),
    # Future paths for adding publications, projects, interests
]
