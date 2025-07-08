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
]