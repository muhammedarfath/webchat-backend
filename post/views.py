from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from post.serializers import PostSerializer
from post.models import Post, Stream
from users_auth.models import User
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class Posts(APIView):
    permission_classes = [AllowAny]
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            if user:
                posts = Stream.objects.filter(user=user)
                post_ids = [post.post.id for post in posts]
                post_items = Post.objects.filter(id__in=post_ids).order_by('-posted') 
                serializer = PostSerializer(post_items, many=True)   
                return Response(serializer.data, status=status.HTTP_200_OK) 
            else:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)      
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)