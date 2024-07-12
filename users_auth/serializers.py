from rest_framework import serializers
from chat.models import User,Profile
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
        fields = ['full_name','date_of_birth', 'bio', 'image']
        
    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.bio = validated_data.get('bio', instance.bio)
        if 'image' in validated_data:
            instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        try:
            user = User.objects.create_user(**validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": f"Error creating user: {str(e)}"})

        profile_instance, created = Profile.objects.get_or_create(user=user, defaults=profile_data)

        if not created:
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)
            profile_instance.save()

        return user