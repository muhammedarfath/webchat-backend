from rest_framework import serializers
from comment.models import Comment
from users_auth.serializers import UsersSerializer,ProfileSerializer
from .models import Likes, Post,Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag 
        fields = ['id', 'title', 'slug'] 


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  
    user = UsersSerializer()
    class Meta:
        model = Post
        fields = ['id', 'media_file', 'caption', 'posted', 'tags', 'user', 'likes']
    
class LikesSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    post = PostSerializer()
    class Meta:
        model = Likes
        fields = ['user','post']    

class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    class Meta:
        model = Comment 
        fields = ['user','body','date']   
    