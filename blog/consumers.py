from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, PrivateMessage, Chatters, Online


# class PrivateConsumer(WebsocketConsumer):
#
#     def fetch_messages(self, data):
#         chat_id = self.scope['url_route']['kwargs']['chat_id']
#         messages = PrivateMessage.objects.filter(chat_id=chat_id).order_by('date_posted')[:10]
#         content = {
#             "command": 'messages',
#             "messages": self.messages_to_json(messages)
#         }
#
#         self.send_message(content)
#
#     def new_message(self, data):
#         chat_id = self.scope['url_route']['kwargs']['chat_id']
#         author = self.scope['user'].username
#         author_user = get_object_or_404(User, username=author)
#         if not PrivateMessage.objects.filter(chat_id=chat_id):
#             message = PrivateMessage.objects.create(author=author_user, content=data['message'], chat_id=chat_id)
#         else:
#             message = PrivateMessage.objects.create(author=author_user, content=data['message'], chat_id=chat_id)
#         content = {
#             'command': 'new_message',
#             'message': self.message_to_json(message)
#         }
#         return self.send_chat_message(content)
#
#     def messages_to_json(self, messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result
#
#     def message_to_json(self, message):
#         return {
#             'author': message.author.username,
#             'content': message.content,
#             'date_posted': str(message.date_posted)
#         }
#
#     commands = {
#         'fetch_messages': fetch_messages,
#         'new_message': new_message
#     }
#
#     def connect(self):
#         self.chat_id = self.scope['url_route']['kwargs']['chat_id']
#         self.room_group_name = 'direct_%s' % self.chat_id
#         self.user = self.scope['user'].username
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     def receive(self, text_data):
#         data = json.loads(text_data)
#         self.commands[data['command']](self, data)
#
#     def send_chat_message(self, message):
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     def send_message(self, message):
#         self.send(text_data=json.dumps(message))
#
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#
#         self.send(text_data=json.dumps(message))
#

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        room_id = self.scope['url_route']['kwargs']['room_name']

        author = self.scope['user'].username
        author_user = get_object_or_404(User, username=author)

        if not Online.objects.filter(roomid=room_id).exists():
            Online.objects.create(roomid=room_id)

        users_online = get_object_or_404(Online,roomid=room_id)
        if not users_online.online_user.filter(id=author_user.id).exists():
            users_online.online_user.add(author_user)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        room_id = self.scope['url_route']['kwargs']['room_name']
        author = self.scope['user'].username
        author_user = get_object_or_404(User, username=author)

        users_online = get_object_or_404(Online,roomid=room_id)
        if users_online.online_user.filter(id=author_user.id).exists():
            users_online.online_user.remove(author_user)

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def fetch_messages(self, data):
        chat_id = self.scope['url_route']['kwargs']['room_name']
        messages = Message.objects.filter(chat_id=chat_id).order_by('-date_posted')[:10]
        content = {
            "command": 'messages',
            "messages": self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        chat_id = self.scope['url_route']['kwargs']['room_name']
        author = self.scope['user'].username
        author_user = get_object_or_404(User, username=author)

        if not Message.objects.filter(chat_id=chat_id):
            message = Message.objects.create(author=author_user, content=data['message'], chat_id=chat_id,roomid=chat_id)
        else:
            message = Message.objects.create(author=author_user, content=data['message'], chat_id=chat_id,roomid=chat_id)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def typing(self,author):
        author = self.scope['user'].username
        author_user = get_object_or_404(User, username=author)

        is_typing = ""
        if author_user:
            is_typing = "typing"
        
        content = {
            'command':'is_typing'
        }

        return content

    def message_to_json(self, message):
        
        return {
            'author': message.author.username,
            'content': message.content,
            'date_posted': str(message.date_posted)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'is_typing': typing,
    }

    

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps(message))
