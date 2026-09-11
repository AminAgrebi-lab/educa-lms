from .base import *

DEBUG = True

# Allow the sample domain during local development as well
ALLOWED_HOSTS = [
    '.educaproject.com',   # wildcard: domain + any subdomain
    '127.0.0.1',
    'localhost',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}