from django import forms
# Make sure Project, InventoryItem, and ProjectPhoto are all imported
from .models import Project, InventoryItem, ProjectPhoto 

class ProjectForm(forms.ModelForm):
    # This creates a field with checkboxes for all of the user's inventory items
    required_inventory = forms.ModelMultipleChoiceField(
        queryset=InventoryItem.objects.none(), # We'll set the real queryset in the view
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        # Add 'required_inventory' to the list of fields
        fields = ['name', 'description', 'status', 'required_inventory']

    def __init__(self, *args, **kwargs):
        # We need to get the user from the view to filter the inventory
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # This is the key part: it makes sure the user only sees their own inventory items as choices
            self.fields['required_inventory'].queryset = InventoryItem.objects.filter(owner=user)

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = ProjectPhoto
        fields = ['image', 'caption']