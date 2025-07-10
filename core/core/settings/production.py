import os
import dj_database_url
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['your-app-name.herokuapp.com']


DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}


# Static files with WhiteNoise
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# CSRF settings for production
CSRF_TRUSTED_ORIGINS = ['https://*.herokuapp.com']