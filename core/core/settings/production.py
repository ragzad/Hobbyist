# core/core/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['https://hobb-2d20ec3f46fe.herokuapp.com/']
STATIC_ROOT = BASE_DIR.parent.parent / 'staticfiles'