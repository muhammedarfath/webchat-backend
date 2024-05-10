from rest_framework import serializers
from .models import User , Profile


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