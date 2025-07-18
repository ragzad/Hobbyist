from django.db import models
from django.contrib.auth.models import User

# --- CATEGORY MODEL ---
class Category(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    icon_class = models.CharField(max_length=50, blank=True, default='bi-box')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Folder(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    folder_type = models.CharField(max_length=20, default='project')

    def __str__(self):
        return self.name

# --- PROJECT MODEL ---
class Project(models.Model):
    STATUS_CHOICES = [('NOT_STARTED', 'Not Started'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    required_inventory = models.ManyToManyField('InventoryItem', blank=True, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to='project_covers/', null=True, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')

    def __str__(self):
        return self.name

# --- INVENTORY ITEM MODEL ---
class InventoryItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    unit_of_measurement = models.CharField(max_length=50, blank=True, help_text="e.g., pcs, g, ml, cm")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_items')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit_of_measurement})"

# --- OTHER MODELS ---

class ProjectPhoto(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='project_photos/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.project.name}"

class Task(models.Model):
    STATUS_CHOICES = [('TODO', 'To Do'), ('INPROGRESS', 'In Progress'), ('DONE', 'Done')]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='TODO')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='task_attachments/', null=True, blank=True)

    def __str__(self):
        return self.title