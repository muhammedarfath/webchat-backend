from django.shortcuts import render
from django.views import View
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from post.serializers import PostSerializer
from post.models import Post
from users_auth.serializers import UserDetailsSerializer
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
                posts = Post.objects.filter(user__username=user_name)
                profile_serializer = UserDetailsSerializer(profile)
                post_serializer = PostSerializer(posts,many=True)
                response_data = {
                    "profile": profile_serializer.data,
                    "posts": post_serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
