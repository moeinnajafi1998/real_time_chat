import json
from channels.generic.websocket import AsyncWebsocketConsumer
from icecream import ic
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import PrivateChat  # Import your model


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        ic(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        ic(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))





# class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the users from the URL route (assumes route is /ws/private_chat/<int:user1_id>/<int:user2_id>/)
        self.user1_id = self.scope['url_route']['kwargs']['user1_id']
        self.user2_id = self.scope['url_route']['kwargs']['user2_id']
        
        # Fetch or create a private chat room
        self.chat_room = await database_sync_to_async(self.get_or_create_chat_room)(self.user1_id, self.user2_id)
        
        # Generate a unique room name
        self.room_group_name = self.chat_room.get_room_name()

        # Add this connection to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_or_create_chat_room(self, user1_id, user2_id):
        user1 = User.objects.get(id=user1_id)
        user2 = User.objects.get(id=user2_id)
        chat_room, _ = PrivateChat.objects.get_or_create(user1=user1, user2=user2)
        return chat_room


from channels.generic.websocket import WebsocketConsumer
import json

class PrivateChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({"message": "Connection established"}))

    def disconnect(self, close_code):
        pass
