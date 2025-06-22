# import json
# from channels.generic.websocket import AsyncWebsocketConsumer 
# from channels.db import database_sync_to_async
# from .models import Room, Message, Profile
# from django.contrib.auth.models import User
# import time
# import datetime

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print("connecting")
#         user = self.scope['user']
#         print(user)
#         await self.update_status_online(user)

#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
        
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         print("disconnected", self, close_code)
#         user = self.scope['user']
#         await self.update_status_offline(user)
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         username = text_data_json['username']
#         room = text_data_json['room']
       

#         # Send message to room group
#         await self.save_message(username, room, message)
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'username': username
#             }
#         )
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']
    
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username,
#             'timestamp': time.strftime("%m.%d.%Y %I:%M %p")
            
#         }))

#     @database_sync_to_async
#     def save_message(self, username, room, message):
#         user=User.objects.get(first_name=username)
#         room=Room.objects.get(name=room)
#         print(user)
#         print(room)
#         Message.objects.create(user=user, room=room, message=message)
   
#     @database_sync_to_async
#     def update_status_online(self, user):
#         user_obj = User.objects.get(username = user)
#         Profile_obj = Profile.objects.filter(user = user_obj.id).update(online = True, offline = False, last_seen = None)
#         print(Profile_obj)

#     @database_sync_to_async
#     def update_status_offline(self, user):
#         user_obj = User.objects.get(username = user)
#         Profile_obj = Profile.objects.filter(user = user_obj.id).update(online = False, offline = True)
#         print(Profile_obj)


import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))