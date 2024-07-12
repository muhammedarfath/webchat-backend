import random
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from project import settings
from chat.models import User
from .serializers import UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str 
# Create your views here.

        
        
        
class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({"error":"check your credentials"},serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error":"somthing went wrong"})
        
    
    
    
    
class OTPVerificationView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            otp_entered = request.data.get('otp')
            email = request.data.get('email')  
            if not otp_entered or not email:
                return Response({"error": "OTP and email are required"}, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, email=email)
            if user.otp == otp_entered:
                user.is_email_verified = True  
                user.save()
                return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
          
class ResentOTP(APIView):
    def post(self,request):
        try:
            email = request.data.get('email')
            print(email)
            if not email:
                return Response({"error":"email are required"},status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, email=email)
            user.otp = None
            if user.email:
                otp = str(random.randint(10000,99999))
                user.otp = otp
                user.save()
                subject = 'Resent OTP Verification Code'
                message = f'Your resent OTP code for signup is: {otp}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]    
                send_mail(subject, message, from_email, recipient_list)
                return Response({"message": "resend OTP sent successfully. Please check your email."},status=status.HTTP_200_OK)
            else:
                return Response({"error":"Failed to resend OTP. Please try again."})
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            

        

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
            'message':"Login Successfully",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'user_id': user.id,
            'user_email': user.email,
            'is_superuser': user.is_superuser,
        }
        return Response(response_data,status=status.HTTP_200_OK)
    
    
    
    
class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get("email")
            user = User.objects.get(email=email)
            if user:
                link = f"http://localhost:3000/password-reset-confirm/{user.id}/"
                send_mail(
                    'Verify Account',
                    'Please verify your account',
                    'fyboxteam@gmail.com',
                    [email],
                    fail_silently=False,
                    html_message=f"<p>Your OTP is </p><p>{link}</p>"
                )
                return Response({'message': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class PasswordResetConfirm(APIView):
    permission_classes = [AllowAny]

    def post(self, request, user_id):
        try:
            password = request.data.get("password")
            if not password:
                return Response({'error': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            
            return Response({'message': 'Password has been changed.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Oops... User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
