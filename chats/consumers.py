import json
import jwt

from django.conf import settings

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

from users.models import CustomUser
from .models import Message
    

class ChatConsumer(AsyncWebsocketConsumer):
    def get_auth_header(self):
        auth_header = dict(self.scope['headers']).get(b'authorization', None)
        if auth_header is None:
            return None
        token = auth_header.decode().split(' ')[1]
        return token

    def get_username_from_token(self):
        token = self.get_auth_header()
        if not token:
            return None
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get('user_id', None)
            return user_id
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
    @database_sync_to_async
    def get_user_by_username(self, username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
        
    @database_sync_to_async
    def save_message(self, message):
        Message(
            sender=self.sender,
            receiver=self.receiver,
            content=message
        ).save()

    async def connect(self):
        query_params = parse_qs(self.scope['query_string'].decode())
        receiver_username = query_params.get('username', [None])[0]
        sender_id = self.get_username_from_token()

        if not receiver_username or not sender_id:
            await self.close()
            return
        
        self.receiver = await self.get_user_by_username(receiver_username)
        self.sender = await self.get_user_by_id(sender_id)
        
        if not self.receiver or not self.sender:
            await self.close()
            return

        self.receiver_group_name = f'private_{self.receiver.username}'
        await self.channel_layer.group_add(
            self.receiver_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        
        if not message:
            return
        
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.receiver_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': str(self.sender.username)
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
