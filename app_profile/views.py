from django.shortcuts import render
from django.views import View
from rest_framework.permissions import AllowAny,IsAuthenticated
from chat.serializers import UserDetailsSerializer
from rest_framework.response import Response
from chat.models import Profile
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.


class UserProfile(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_name = request.data.get('username')
        try:
            if user_name:
                profile = Profile.objects.get(user__username=user_name)
                print(profile,"ussssssss")
                serializer = UserDetailsSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
