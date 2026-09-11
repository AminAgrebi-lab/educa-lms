# Import every common setting defined in base.py
from .base import *

# Local development: debug mode ON and the SQLite database
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}