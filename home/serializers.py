from rest_framework import serializers
from chat.serializers import ProfileSerializer
from chat.models import Message




class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['author','recipient', 'content', 'timestamp']
