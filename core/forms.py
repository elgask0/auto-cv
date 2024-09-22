# core/forms.py

from django import forms
from .models import UserProfile, Education, Experience
from django.forms import inlineformset_factory

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'name', 
            'phone', 
            'linkedin_link', 
            'summary', 
            'skills', 
            'publications', 
            'projects', 
            'interests',
            'city',        # Added
            'state',       # Added
            'postal_code', # Optional
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1234567890'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/yourprofile'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'A brief summary about yourself...'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g., Python; Django; REST APIs'}),
            'publications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List publications separated by ; or new lines.'}),
            'projects': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List projects separated by ; or new lines.'}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List interests separated by ; or new lines.'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),        # Added
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),      # Added
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),  # Optional
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            'education_level', 'university', 'city', 'state', 
            'start_date', 'end_date', 'specialization', 'thesis', 'relevant_subjects'
        ]
        widgets = {
            'education_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Bachelor, Master'}),
            'university': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., University of XYZ'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specialization (optional)'}),
            'thesis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thesis Title (optional)'}),
            'relevant_subjects': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'List relevant subjects...'}),
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
        fields = [
            'company', 'city', 'state', 'title', 
            'start_date', 'end_date', 'description'
        ]
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Tech Innovators Inc.'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Senior Software Engineer'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your role and responsibilities...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")

# Define inline formsets for Education and Experience
EducationFormSet = inlineformset_factory(
    UserProfile,
    Education,
    form=EducationForm,
    extra=0,  # Set to 0 to prevent extra forms on page load
    can_delete=True,
)

ExperienceFormSet = inlineformset_factory(
    UserProfile,
    Experience,
    form=ExperienceForm,
    extra=0,  # Set to 0 to prevent extra forms on page load
    can_delete=True,
)

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
        initial=True,  # Checked by default
        label='Generate CV'
    )
    
    generate_cover_letter = forms.BooleanField(
        required=False,
        initial=True,  # Checked by default
        label='Generate Cover Letter'
    )
    
    fast_mode = forms.BooleanField(
        required=False,
        initial=False,  # Unchecked by default
        label='Fast Mode'
    )