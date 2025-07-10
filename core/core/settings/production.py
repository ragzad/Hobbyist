# core/core/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['https://git.heroku.com/hobb.git']
STATIC_ROOT = BASE_DIR.parent.parent / 'staticfiles'