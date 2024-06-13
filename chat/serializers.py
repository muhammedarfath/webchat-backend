from rest_framework import serializers
from .models import Profile,Message
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','phone','is_active']
        extra_kwargs = {'password':{'write_only':True}}
        

class UserDetailsSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Profile
        fields = "__all__"
        depth = 1
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile    
        fields = ['full_name', 'bio', 'image']
        
    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.bio = validated_data.get('bio', instance.bio)
        if 'image' in validated_data:
            instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
   
   
class MessageSerializer(serializers.ModelSerializer):
        profile = ProfileSerializer()
        author = UsersSerializer()
        recipient = UsersSerializer()
        class Meta:
            model = Message    
            fields = ['author', 'profile', 'recipient','content','timestamp']
            depth = 1  