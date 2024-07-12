from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .forms import NewPostForm
from post.serializers import PostSerializer
from post.models import Post, Stream, Tag
from users_auth.models import User
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class Posts(APIView):
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
        
        
        
class NewPost(APIView):
    def post(self,request,username):
        print(username)
        try:
            user = User.objects.get(username=username)
            tags_objs = []
            if user:
                picture = request.FILES.get('picture')
                caption = request.data.get('caption')
                tags_form = request.data.get('tags')
                 
                print(picture)
                
                tags_list = list(tags_form.split(','))
                
                for tag in tags_list:
                    t,created = Tag.objects.get_or_create(title=tag)
                    tags_objs.append(t)
                p,created = Post.objects.get_or_create(picture=picture,caption=caption,user=user)  
                p.tags.set(tags_objs)
                p.save()
                return Response({"message":"post added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"User not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
        
            