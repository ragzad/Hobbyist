from django.contrib import admin
from .models import Project, InventoryItem, Category, Task

admin.site.register(Project)
admin.site.register(InventoryItem)
admin.site.register(Task)