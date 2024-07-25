from rest_framework import serializers
from .models import User,Profile
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
    user=UsersSerializer(required=False)
    class Meta:
        model = Profile    
        fields = ['user','full_name','date_of_birth', 'bio', 'image']
        
        
class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'profile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        old_email = instance.email 
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        if old_email != instance.email:
            self.clean_old_email(old_email)
        if profile_data:
            profile_instance = instance.profile
            profile_instance.full_name = profile_data.get('full_name', profile_instance.full_name)
            profile_instance.bio = profile_data.get('bio', profile_instance.bio)
            if 'image' in profile_data:
                profile_instance.image = profile_data['image']
            profile_instance.save()

        return instance
    def clean_old_email(self,old_email):
        try:
            user = User.objects.get(email=old_email)
            user.email = None 
            user.save()
        except User.DoesNotExist:
            pass


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone', 'profile')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        print(profile_data)
        username = validated_data['username']
        email = validated_data['email']
        phone = validated_data['phone']
        user = User.objects.create(
            username = username,
            email = email,
            phone = phone
        )
        password = validated_data['password']
        user.set_password(password)
        user.save()
        profile_instance, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
        if not created:
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)
            profile_instance.save()    
        return {'user': user, 'profile': profile_instance}
    def to_representation(self, instance):
        user = instance['user']
        profile = instance['profile']
        user_data = super(UserRegistrationSerializer, self).to_representation(user)
        profile_data = ProfileSerializer(profile).data if profile else None
        user_data['profile'] = profile_data
        return user_data