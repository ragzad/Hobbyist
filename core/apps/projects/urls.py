# apps/projects/urls.py
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('create/', views.ProjectCreateView.as_view(), name='project-create'), # Add this line
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
]