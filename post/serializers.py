from rest_framework import serializers
from users_auth.serializers import UsersSerializer
from .models import Post,Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag 
        fields = ['id', 'title', 'slug'] 


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    user = UsersSerializer()
    class Meta:
        model = Post
        fields = ['id', 'picture', 'caption', 'posted', 'tags', 'user', 'likes']
    