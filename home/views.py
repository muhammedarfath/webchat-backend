from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q

from chat.serializers import ProfileSerializer
from .serializers import MessageSerializer
from chat.models import Message, Profile
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class LastThreeMessages(APIView):
    permission_classes = [AllowAny]

    def get(self, request, userId):
        try:
            user_profile = Profile.objects.get(user__id=userId)

            messages = Message.objects.filter(
                Q(author=user_profile.user) | Q(recipient=user_profile.user)
            ).order_by('-timestamp')[:3]

            # Extract author and recipient profiles without redundant queries
            author_profiles = {message.author_id: Profile.objects.get(user=message.author) for message in messages}
            recipient_profiles = {message.recipient_id: Profile.objects.get(user=message.recipient) for message in messages}

            message_serializer = MessageSerializer(messages, many=True)
            profile_serializer = ProfileSerializer(list(author_profiles.values()) + list(recipient_profiles.values()), many=True)

            data = {
                "messages": message_serializer.data,
                "profiles": profile_serializer.data,  # Including both authors and recipients profiles
            }
            return Response(data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
