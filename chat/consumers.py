# chat/consumers.py
import json
from .models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message


class ChatConsumer(WebsocketConsumer):
    
    def fetch_messages(self,data):
        print('7')
        author_id, recipient_id = self.room_name.split('_')
        messages = Message.messages_for_room(author_id, recipient_id)

        content = {
            'command':'messages',
            'messages':self.messages_to_json(messages)
        }
        self.send_message(content)
        
    
    def new_message(self,data):
        print('8')
        author_id, recipient_id = self.room_name.split('_')
        author_user = User.objects.get(id=author_id)
        sender_user = User.objects.get(id=recipient_id)
        message = Message.objects.create(author=author_user,recipient=sender_user,content=data['message'])
        content = {
            'command':'new_message',
            'message':self.message_to_json(message)
        }               
        return self.send_chat_message(content)

    
    
    def messages_to_json(self,messages):
        print('9')
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result 
    
    
    def message_to_json(self,message):
        print('10')
        return {
            'author':message.author.username,
            'recipient':message.recipient.username,
            'content':message.content,
            'timestamp':str(message.timestamp)
            
            }   
        
    
    commands = {
        'fetch_messages':fetch_messages,
        'new_message': new_message
    }
    
    
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        sender_id, recipient_id = self.room_name.split('_')
         #creating room 
        self.room_group_name = f"chat_{min(sender_id, recipient_id)}_{max(sender_id, recipient_id)}"
        print(self.room_group_name,"this is group")
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print('2')
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )



    def receive(self, text_data):
        print('3')
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        
        
        
        
        
    def send_chat_message(self,message): 
        print('4')   
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )


    def send_message(self,message):
        print('5')
        self.send(text_data=json.dumps( message))
        
    
    
    
    def chat_message(self, event):
        print('6')
        message = event["message"]
        self.send(text_data=json.dumps( message))