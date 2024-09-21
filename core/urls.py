# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('generate-documents/', views.generate_documents, name='generate_documents'),
    path('documents/', views.document_list, name='document_list'),
    path('render-latex/<int:generation_id>/', views.render_latex, name='render_latex'),
    path('download-pdf/<int:generation_id>/', views.download_pdf, name='download_pdf'),
]
