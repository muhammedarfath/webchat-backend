from rest_framework import serializers
from chat.serializers import ProfileSerializer
from chat.models import User,Profile



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