from django.db import models
from django.contrib.auth.models import User

# A common pattern to extend Django's built-in User model
class Profile(models.Model):
    # Creates a one-to-one link to a User. If a User is deleted, their profile is also deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # A simple boolean to track if the user has paid for premium features.
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# The main model for a single hobby project.
class Project(models.Model):
    # Choices for the project status field
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    # A many-to-one link. One User can own many Projects.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    # A simple text field for the project's name.
    name = models.CharField(max_length=200)
    # A larger text field for a detailed description.
    description = models.TextField(blank=True, null=True) # blank=True allows the form field to be empty.
    # The project's current status, using the choices defined above.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    # These fields automatically record the creation and last update times.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Represents a single item in a user's inventory (e.g., a paint bottle, a component).
class InventoryItem(models.Model):
    # Links the inventory item to a user.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_items')
    # The name of the item.
    name = models.CharField(max_length=200)
    # How many of this item the user owns.
    quantity = models.PositiveIntegerField(default=1)
    # An optional field for any notes.
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name