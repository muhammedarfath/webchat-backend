from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q

from chat.serializers import UserDetailsSerializer
from .serializers import MessageSerializer
from chat.models import Message, Profile
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


# class LastThreeMessages(APIView):
#     permission_classes = [AllowAny]
#     def get(self, request, userId):
#         try:
#             user_profile = Profile.objects.get(user__id=userId)

#             messages = Message.objects.filter(
#                 Q(author=user_profile.user) | Q(recipient=user_profile)
#             ).order_by('-timestamp')[:3]
            
        
#             serializer = MessageSerializer(messages, many=True)
#             # print(serializer.data)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Profile.DoesNotExist:
#             return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        
        
        
class LastThreeMessages(APIView):
    permission_classes = [AllowAny]

    def get(self, request,userId):
        print(userId)
        if userId is not None:
            try:
                messages = Message.objects.filter(
                    Q(author_id=userId) | Q(recipient__user_id=userId)
                ).order_by('-timestamp')[:3]
                
                print(messages,"this is some")
                
                
                if messages.exists():
                    serialized_profiles = []
                    message_users = set()
                    for message in messages:
                        participants = [message.author, message.recipient.user]
                        for participant in participants:
                            if participant and participant.id != userId and participant.id not in message_users:
                                profile = Profile.objects.get(user=participant)
                                serialized_profiles.append(UserDetailsSerializer(profile).data)
                                message_users.add(participant.id)
                    return Response(serialized_profiles, status=status.HTTP_200_OK)
                else:
                    return Response([], status=status.HTTP_204_NO_CONTENT)
            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "current_userId not provided in request data."}, status=status.HTTP_400_BAD_REQUEST)
        
                