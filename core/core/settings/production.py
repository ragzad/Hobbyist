# core/settings/production.py

import os
import dj_database_url
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'


# NOTE: For a real production app you would lock this down further.
ALLOWED_HOSTS = ['*']


CSRF_TRUSTED_ORIGINS = ['https://hobb-5e258a5700a4.herokuapp.com']


DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Static files settings for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add WhiteNoise to middleware
# Make sure it's placed after SecurityMiddleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')