from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from chat.models import User
from .serializers import UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib.auth import get_user_model
from django.http import JsonResponse

# Create your views here.

User = get_user_model()

class CheckUsernameView(APIView):
    def get(self, request, *args, **kwargs):
        username = self.request.GET.get('username', None)
        if not username:
            return JsonResponse({'error': 'Username parameter is required'}, status=400)

        try:
            user = User.objects.get(username=username)
            return JsonResponse({'exists': True})
        except User.DoesNotExist:
            return JsonResponse({'exists': False})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
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