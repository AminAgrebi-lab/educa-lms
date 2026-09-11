# Import every common setting defined in base.py
from .base import *

# PRODUCTION: never expose tracebacks or configuration secrets
DEBUG = False

# Error emails go to these people when DEBUG is False
ADMINS = [
    ('Your Admin', 'admin@yourdomain.com'),  # Replace with your own contact
]

# TEMPORARY: accept any host; restricted to your real domain later
ALLOWED_HOSTS = ['*']

# TEMPORARY: still SQLite; PostgreSQL via Docker Compose comes later
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 🚨 BOOK TYPO fixed: reading prints 'NAME: BASE_DIR / ... (missing quote and =)
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}