"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import sys
from django.core.asgi import get_asgi_application

# Calculate the path to the 'outer core' directory (e.g., /app/core/).
outer_core_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the 'outer core' directory to sys.path.
sys.path.insert(0, outer_core_dir)

# Add the 'apps' directory within 'core' to sys.path.
sys.path.insert(0, os.path.join(outer_core_dir, 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')

application = get_asgi_application()