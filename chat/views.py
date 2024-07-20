from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from post.models import Follow
from users_auth.serializers import UserDetailsSerializer
from .models import Message
from users_auth.models import Profile
from django.db.models import Q




class Users(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        current_user_id = request.data.get('current_userId')
        if current_user_id is not None:
            try:
                messages = Message.objects.filter(
                    Q(author_id=current_user_id) | Q(recipient__user_id=current_user_id)
                )
                if messages.exists():
                    serialized_profiles = []
                    message_users = set()
                    for message in messages:
                        participants = [message.author, message.recipient.user]
                        for participant in participants:
                            if participant and participant.id != current_user_id and participant.id not in message_users:
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


class FriendUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        current_userId = request.data.get('current_userId')
        if username is not None:
            try:
                messages = Message.objects.filter(
                    Q(author_id=current_userId) & Q(recipient__user__username=username)
                )
                print(messages,"is it empty")
                serialized_profiles = []
                if messages:
                    print("looooooooo")
                    message_users = set()
                    for message in messages:
                        participants = [message.author, message.recipient.user]
                        for participant in participants:
                            if participant and participant.id != username and participant.id not in message_users:
                                profile = Profile.objects.get(user=participant)
                                serialized_profiles.append(UserDetailsSerializer(profile).data)
                                message_users.add(participant.id)
                    return Response(serialized_profiles, status=status.HTTP_200_OK)
                else:
                    profile = Profile.objects.get(user__username=username)
                    serialized_profiles.append(UserDetailsSerializer(profile).data)
                    return Response(serialized_profiles, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "current_userId not provided in request data."}, status=status.HTTP_400_BAD_REQUEST)

            
        
        
class Suggested(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        current_user_id = request.data.get('current_userId')
        search_query = request.data.get('search_query', '')
        if current_user_id is not None:
            try:
                profiles = Profile.objects.exclude(user=current_user_id)
                response_data = []
                if search_query:
                    profiles = profiles.filter(user__username__icontains=search_query)
                for profile in profiles:      
                    serializer = UserDetailsSerializer(profile)
                    post_data = serializer.data
                    post_data['follow_status'] = Follow.objects.filter(following=profile.user,follower__id=current_user_id).exists()
                    response_data.append(post_data)
                return Response(response_data, status=status.HTTP_200_OK)

            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=404)
        else:
            return Response({"error": "current_userId not provided in request data."}, status=400)


        
    


        
        
class RoomView(APIView):
    permission_classes = [AllowAny]
    def post(self, request,room_name):
        user_id = request.data.get('user_id')
        if user_id is not None:
            try:
                user = Profile.objects.get(id=user_id)
                serializer = UserDetailsSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=404)
        else:     
           return Response({"error": "current_userId not provided in request data."}, status=400) 
