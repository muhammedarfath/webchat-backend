from rest_framework import serializers
from .models import User , Profile,Message


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','is_active']
        extra_kwargs = {'password':{'write_only':True}}
        
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                email=validated_data['email'],
                )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    class Meta:
        model = Profile
        fields = '__all__'
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
    sender_profile = ProfileSerializer(read_only=True)
    receiver_profile = ProfileSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id','user','sender','sender_profile','receiver_profile','receiver','content','is_read','timestamp']
    