import json
# Wrapper to call async channel layer methods from a sync consumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
# Timezone-aware current time for stamping messages
from django.utils import timezone


class ChatConsumer(WebsocketConsumer):
    """Handles WebSocket connections for a course chat room."""

    def connect(self):
        # AuthMiddlewareStack injected the logged-in user into the scope
        self.user = self.scope['user']
        # Course id from the WebSocket URL kwargs
        self.id = self.scope['url_route']['kwargs']['course_id']
        # One group per course chat room
        self.room_group_name = f'chat_{self.id}'
        # Join the group with this connection's channel
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave the group when the connection closes
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Server-side timestamp in ISO 8601 format
        now = timezone.now()
        # Broadcast message + sender + time to the whole group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    def chat_message(self, event):
        # Auto-invoked on every consumer in the group; forward to WebSocket
        self.send(text_data=json.dumps(event))