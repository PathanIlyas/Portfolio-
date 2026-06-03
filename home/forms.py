from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Project, CustomUser, Skill, Profile

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'advance-input w-100', 'placeholder': 'admin@example.com'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'advance-input w-100', 'placeholder': '••••••••'}))

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link', 'image', 'github_link', 'featured', 'order', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'advance-input', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'advance-input', 'rows': 4, 'placeholder': 'Project Description'}),
            'link': forms.URLInput(attrs={'class': 'advance-input', 'placeholder': 'https://example.com'}),
            'image': forms.ClearableFileInput(attrs={'class': 'advance-input'}),
            'github_link': forms.URLInput(attrs={'class': 'advance-input', 'placeholder': 'https://github.com/Username/repo'}),
            'featured': forms.CheckboxInput(attrs={'style': 'width: 20px; height: 20px; cursor: pointer; accent-color: var(--accent-cyan);'}),
            'order': forms.NumberInput(attrs={'class': 'advance-input', 'placeholder': '0'}),
            'tags': forms.TextInput(attrs={'class': 'advance-input', 'placeholder': 'Django, Python, Rest API'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'percentage', 'icon_class', 'color', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'advance-input', 'placeholder': 'Skill Name (e.g. Django)'}),
            'category': forms.Select(attrs={'class': 'advance-input'}),
            'percentage': forms.NumberInput(attrs={'class': 'advance-input', 'min': 0, 'max': 100, 'placeholder': '85'}),
            'icon_class': forms.TextInput(attrs={'class': 'advance-input', 'placeholder': 'fa-brands fa-python'}),
            'color': forms.TextInput(attrs={'class': 'advance-input', 'placeholder': '#00f3ff'}),
            'order': forms.NumberInput(attrs={'class': 'advance-input'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name', 'title', 'tagline', 'bio', 'email', 'github', 'linkedin', 
            'profile_image', 'resume', 'available', 'years_experience', 
            'projects_completed', 'clients_served'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'advance-input', 'placeholder': 'Your Name'}),
            'title': forms.TextInput(attrs={'class': 'advance-input', 'placeholder': 'Job Title'}),
            'tagline': forms.TextInput(attrs={'class': 'advance-input', 'placeholder': 'Short Tagline'}),
            'bio': forms.Textarea(attrs={'class': 'advance-input', 'rows': 4, 'placeholder': 'Short Bio'}),
            'email': forms.EmailInput(attrs={'class': 'advance-input', 'placeholder': 'email@example.com'}),
            'github': forms.URLInput(attrs={'class': 'advance-input', 'placeholder': 'https://github.com/Username'}),
            'linkedin': forms.URLInput(attrs={'class': 'advance-input', 'placeholder': 'https://linkedin.com/in/Username'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'advance-input'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'advance-input'}),
            'available': forms.CheckboxInput(attrs={'style': 'width: 20px; height: 20px; cursor: pointer; border-radius: 4px; border: 1px solid var(--card-border); accent-color: var(--accent-cyan);'}),
            'years_experience': forms.NumberInput(attrs={'class': 'advance-input'}),
            'projects_completed': forms.NumberInput(attrs={'class': 'advance-input'}),
            'clients_served': forms.NumberInput(attrs={'class': 'advance-input'}),
        }

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'advance-input w-100', 'placeholder': 'client@example.com'}),
            'first_name': forms.TextInput(attrs={'class': 'advance-input w-100', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'advance-input w-100', 'placeholder': 'Last Name'}),
        }
