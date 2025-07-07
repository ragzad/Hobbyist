# core/urls.py
from django.contrib import admin
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.users.urls')),
    path('upgrade/', include('apps.payments.urls')),
    path('projects/', include('apps.projects.urls')), 
]

# This is only for development, to serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)