from django.urls import re_path
from . import consumers

# WebSocket URL patterns (handled by Channels, not Django's urls.py)
websocket_urlpatterns = [
    re_path(
        r'ws/chat/room/(?P<course_id>\d+)/$',
        consumers.ChatConsumer.as_asgi()
    ),
]