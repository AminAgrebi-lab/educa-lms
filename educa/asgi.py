"""
ASGI config for educa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

# Channels router: maps protocol types (http/websocket) to ASGI apps
from channels.routing import ProtocolTypeRouter
# Django's built-in ASGI application for standard HTTP requests
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educa.settings')

# Initialize Django's ASGI app (before building the router)
django_asgi_app = get_asgi_application()

# Root ASGI application: route each protocol to its handler
application = ProtocolTypeRouter({
    # Standard HTTP requests keep flowing to your existing Django views
    'http': django_asgi_app,
    # 'websocket': will be wired in the next reading (Writing a Consumer)
})