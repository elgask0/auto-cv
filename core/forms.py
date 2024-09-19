# core/forms.py

from django import forms
from .models import UserProfile, Education, Experience

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone', 'linkedin_link', 'summary', 'skills', 'publications', 'projects', 'interests']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'publications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'projects': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['education_level', 'university', 'start_date', 'end_date', 'specialization', 'thesis', 'relevant_subjects']
        widgets = {
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'thesis': forms.TextInput(attrs={'class': 'form-control'}),
            'relevant_subjects': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'city', 'title', 'start_date', 'end_date', 'description']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")

class GenerationForm(forms.Form):
    GENERATION_TYPE_CHOICES = [
        ('cv', 'Curriculum Vitae'),
        ('cover_letter', 'Cover Letter'),
    ]
    
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        label='Job Description',
        help_text='Enter the job description for which you are applying.'
    )
    
    generate_cv = forms.BooleanField(
        required=False,
        initial=True,
        label='Generate CV'
    )
    
    generate_cover_letter = forms.BooleanField(
        required=False,
        label='Generate Cover Letter'
    )