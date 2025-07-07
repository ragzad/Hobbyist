# core/urls.py
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.users.urls')),
    path('projects/', include('apps.projects.urls')), 
]