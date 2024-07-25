# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        print(user)
        if not user.is_authenticated:
            return
        
        self.accept()
    
    
    def disconnect(self, close_code):
        pass