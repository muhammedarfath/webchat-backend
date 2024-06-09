# chat/consumers.py
import json
from .models import Notification, Profile, User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message





class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        author_id, recipient_id = self.room_name.split('_')
        recipient_profile = Profile.objects.get(user_id=recipient_id)
        messages = Message.messages_for_room(author_id, recipient_profile.id)
        
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
        
    def new_message(self, data):
        author_id, recipient_id = self.room_name.split('_')
        author_user = User.objects.get(id=author_id)
        recipient_profile = Profile.objects.get(user_id=recipient_id)
        message = Message.objects.create(
            author=author_user,
            recipient=recipient_profile,
            content=data['message']
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)
    
    def messages_to_json(self, messages):
        return [self.message_to_json(message) for message in messages]
    
    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'recipient': message.recipient.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }
    
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }
    
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        sender_id, recipient_id = self.room_name.split('_')
        self.room_group_name = f"chat_{min(sender_id, recipient_id)}_{max(sender_id, recipient_id)}"
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
    
    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))



class NotificationConsumer(WebsocketConsumer):
    
    def fetch_notificaion(self, data):
        userId = self.user_id
        notification = Notification.notification_for_room(userId)
        content = {
            'command': 'notification',
            'messages': self.messages_to_json(notification)
        }
        self.send_message(content)

    def messages_to_json(self, notification):
        result = []
        for notify in notification:
            result.append(self.message_to_json(notify))
        return result 

    def message_to_json(self, notify):
        return {
            'user': notify.user.username,
            'message': notify.message,
            'timestamp': str(notify.timestamp)
        } 

    def send_message(self, notify):
        self.send(text_data=json.dumps(notify))

    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f"user_{self.user_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        print(f"WebSocket connected for user: {self.user_id}")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected for user: {self.user_id}")

    def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command', None)
        if command in self.commands:
            self.commands[command](self, data)
        else:
            print(f"Unknown command received: {command}")

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                "type": "notify_message", 
                "message": message
            }
        )

    def notify_message(self, event):
        message = event["message"]
        print(f"Sending message: {message}")
        self.send(text_data=json.dumps(message))

    def new_notify(self, data):
        userId = self.user_id
        user = User.objects.get(id=userId)
        notify = Notification.objects.create(user=user, message=data['message'])
        content = {
            'command': 'new_notify',
            'message': self.message_to_json(notify)
        }
        self.send_chat_message(content)

    commands = {
        'fetch_notificaion': fetch_notificaion,
        'new_notify': new_notify,
    }