# apps/projects/urls.py
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # --- Project URLs ---
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),

    # --- INVENTORY URLS ---
    path('inventory/', views.InventoryListView.as_view(), name='inventory-list'),
    path('inventory/add/', views.InventoryItemCreateView.as_view(), name='inventory-create'),
    path('inventory/<int:pk>/update/', views.InventoryItemUpdateView.as_view(), name='inventory-update'),
    path('inventory/<int:pk>/delete/', views.InventoryItemDeleteView.as_view(), name='inventory-delete'),

    # --- TASK URLS ---
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/move/', views.move_task, name='task-move'), 

    # --- FOLDER URLS ---
    path('folder/create/', views.create_folder, name='folder-create'),
    path('project/move/', views.move_project_to_folder, name='project-move'),
    path('inventory/move/', views.move_inventory_item_to_folder, name='inventory-move'),
]