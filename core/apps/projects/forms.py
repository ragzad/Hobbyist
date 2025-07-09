from django import forms
from django.db import models
from .models import Project, InventoryItem, ProjectPhoto, Category, Task

# --- PROJECT FORM ---
class ProjectForm(forms.ModelForm):
    required_inventory = forms.ModelMultipleChoiceField(
        queryset=InventoryItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'cover_image', 'required_inventory']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['required_inventory'].queryset = InventoryItem.objects.filter(owner=user)
            # Hide the cover image field if the user is not premium
            if not user.profile.is_premium:
                self.fields['cover_image'].widget = forms.HiddenInput()
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'required_inventory']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['required_inventory'].queryset = InventoryItem.objects.filter(owner=user)

# --- PHOTO UPLOAD FORM ---
class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = ProjectPhoto
        fields = ['image', 'caption']

# --- INVENTORY ITEM FORM ---
class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'quantity', 'unit_of_measurement', 'cost', 'notes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(models.Q(owner=user) | models.Q(owner=None))

# --- TASK FORM ---
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'image']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.profile.is_premium:
            self.fields['image'].widget = forms.HiddenInput()