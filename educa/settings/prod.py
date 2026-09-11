# Read environment variables injected by Docker Compose or a local .env file
from decouple import config
from .base import *

# PRODUCTION: never expose tracebacks or configuration secrets
DEBUG = False

# Error emails go to these people when DEBUG is False
ADMINS = [
    ('Your Name', 'you@yourdomain.com'),  # Replace with your own contact
]

# TEMPORARY: accept any host; restricted to your real domain later
ALLOWED_HOSTS = ['*']

# Production database: PostgreSQL served by the 'db' compose service.
# Locally, a .env file can override HOST/PORT to point at a cloud provider.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        # Inside Docker Compose: hostname of the db container.
        # Locally: override via POSTGRES_HOST in your .env (e.g. Neon)
        'HOST': config('POSTGRES_HOST', default='db'),
        'PORT': config('POSTGRES_PORT', default=5432, cast=int),
        # Encrypted connection: required by cloud providers;
        # the official postgres image supports it too
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Production Redis: 'cache' compose service by default;
# override locally via REDIS_URL in .env (your native Windows Redis)
REDIS_URL = config('REDIS_URL', default='redis://cache:6379')
CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]