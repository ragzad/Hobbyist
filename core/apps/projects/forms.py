from django import forms
from .models import Project, ProjectPhoto

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status']

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = ProjectPhoto
        fields = ['image', 'caption']