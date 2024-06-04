from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Message, Profile, User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserDetailsSerializer,UsersSerializer,ProfileSerializer


class Users(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        current_user_id = request.data.get('current_userId')
        if current_user_id is not None:
            try:
                messages = Message.objects.filter(recipient=current_user_id)
                if messages.exists():
                    serialized_profiles = []
                    message_users = set()
                    for message in messages:
                        author = message.author
                        if author.id not in message_users:
                            profile = Profile.objects.get(user=author)
                            serialized_profiles.append(UserDetailsSerializer(profile).data)
                            message_users.add(author.id)
                    return Response(serialized_profiles, status=status.HTTP_200_OK)
                else:
                    return Response([], status=status.HTTP_204_NO_CONTENT)
            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "current_userId not provided in request data."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class Suggested(APIView):
    permission_classes = [ AllowAny]
    def post(self,request):
        current_user = request.data.get('current_userId')
        if current_user is not None:
            try:
                profiles = Profile.objects.all().exclude(user=current_user)
                serializer = UserDetailsSerializer(profiles,many=True)     
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=404)
        else:
            return Response({"error": "current_userId not provided in request data."}, status=400) 
                   
class FollowRequest(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        current_user_id = request.data.get('followerId')
        friend_user_id = request.data.get('userId')

        if current_user_id is not None and friend_user_id is not None:
            try:
                friend_profile = Profile.objects.get(id=friend_user_id)
                current_profile = Profile.objects.get(id=current_user_id)
                

                current_profile.following.add(friend_profile.user)
                friend_profile.followers.add(current_profile.user)


                serializer = ProfileSerializer(friend_profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Both current_userId and userId are required'}, status=status.HTTP_400_BAD_REQUEST)
            

class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username and password:
            return Response({'error':"fields cannot be empty"},status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                user = User.objects.get(username=username)
                
            except User.DoesNotExist:
                return Response({'error':"invalid cridentials"},status=status.HTTP_401_UNAUTHORIZED) 
        if not user.check_password(password):
            return Response({'error':"invalid cridentials"},status=status.HTTP_401_UNAUTHORIZED)  
        refresh = RefreshToken.for_user(user)
               
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'user_id': user.id,
            'user_email': user.email,
            'is_superuser': user.is_superuser,
        }
        return Response(response_data,status=status.HTTP_200_OK)

class EditProfile(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id):
        profile = get_object_or_404(Profile, user=id)
        serializer = ProfileSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class RoomView(APIView):
    permission_classes = [AllowAny]
    def post(self, request,room_name):
        user_id = request.data.get('user_id')
        print(user_id,"this is user iddddddd")
        if user_id is not None:
            try:
                user = Profile.objects.get(user__id=user_id)
                serializer = UserDetailsSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=404)
        else:     
           return Response({"error": "current_userId not provided in request data."}, status=400) 
