import json
# Async base class: non-blocking I/O, no threads needed per connection
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from chat.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    """Fully asynchronous WebSocket consumer for course chat rooms."""

    async def connect(self):
        # AuthMiddlewareStack injected the logged-in user into the scope
        self.user = self.scope['user']
        # Course id from the WebSocket URL kwargs
        self.id = self.scope['url_route']['kwargs']['course_id']
        # One group per course chat room
        self.room_group_name = 'chat_%s' % self.id
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def persist_message(self, message):
        # acreate() = the asynchronous version of create()
        await Message.objects.acreate(
            user=self.user, course_id=self.id, content=message
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            },
        )
        await self.persist_message(message)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))