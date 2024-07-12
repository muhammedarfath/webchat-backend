from rest_framework import serializers
from users_auth.serializers import ProfileSerializer, UsersSerializer
from .models import Message

   
   
class MessageSerializer(serializers.ModelSerializer):
        profile = ProfileSerializer()
        author = UsersSerializer()
        recipient = UsersSerializer()
        class Meta:
            model = Message    
            fields = ['author', 'profile', 'recipient','content','timestamp']
            depth = 1  