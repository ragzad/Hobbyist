"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

outer_core_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, outer_core_dir)

sys.path.insert(0, os.path.join(outer_core_dir, 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')

application = get_wsgi_application()