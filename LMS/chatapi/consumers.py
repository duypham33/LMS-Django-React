
from app.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Chat
from datetime import datetime

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        chat = Chat.objects.filter(pk = int(data["chat_id"])).first()

        messages = chat.last_10_messages()
        content = {
            'command': 'messages',
            'action': 'fetch_messages',
            'chatID': data["chat_id"],
            'messages': self.messages_to_json(messages)
        }
        self.send_chat_messages(content)

    def new_message(self, data):
        author_user = User.objects.filter(pk = int(data['userID'])).first()
        chat_room = Chat.objects.filter(pk = int(data["chatID"])).first()
    
        Message.objects.create(author=author_user, chat_room=chat_room, content=data['content'])
        chat_room.latestSent = datetime.now()
        chat_room.save()

        messages = chat_room.last_10_messages()
        content = {
            'command': 'messages',
            'chatID': data["chatID"],
            'messages': self.messages_to_json(messages)
        }
        self.send_chat_messages(content)


    def messages_to_json(self, messages):
        return [self.message_to_json(msg) for msg in messages]

    def message_to_json(self, message):
        author = message.author

        return {
            'id': message.pk,
            'author': {
                'id': author.pk,
                'name': author.get_name(),
                'avatar': author.avatar.name
            },
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['chatID']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        self.commands[data['command']](self, data)
        

    def send_chat_messages(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_messages',
                'message': message
            }
        )

    def chat_messages(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
        
    # def send_fetch_messages(self, messages):
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'fetch_messages',
    #             'messages': messages
    #         }
    #     )

    # def fetch_messages(self, event):
    #     self.send(text_data=json.dumps(event['messages']))



class NoticeConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['userID']
        self.room_group_name = 'notice_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def send_notice(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))