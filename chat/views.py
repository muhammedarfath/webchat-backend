from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserDetailsSerializer,UsersSerializer,ProfileSerializer
 
class Users(APIView):
    permission_classes = [ AllowAny]
    def post(self,request):
        current_user = request.data.get('current_userId')
        if current_user is not None:
            try:
                current_profile = Profile.objects.get(id=current_user)
                if current_profile.followers.exists():
                    profiles = Profile.objects.all().exclude(user=current_user)
                    serializer = UserDetailsSerializer(profiles,many=True)     
                    return Response(serializer.data)
                else:
                    return Response([])
            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=404)
        else:
            return Response({"error": "current_userId not provided in request data."}, status=400) 
        
        
        
class Suggested(APIView):
    permission_classes = [ AllowAny]
    def post(self,request):
        current_user = request.data.get('current_userId')
        if current_user is not None:
            try:
                profiles = Profile.objects.all().exclude(user=current_user)
                serializer = UserDetailsSerializer(profiles,many=True)     
                return Response(serializer.data)

            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=404)
        else:
            return Response({"error": "current_userId not provided in request data."}, status=400) 
                   
           

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
        if user_id is not None:
            try:
                user = Profile.objects.get(user=user_id)  
                serializer = UserDetailsSerializer(user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({"error": "Current user profile not found."}, status=404)
        else:     
           return Response({"error": "current_userId not provided in request data."}, status=400) 
