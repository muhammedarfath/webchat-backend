from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from post.serializers import LikesSerializer, PostSerializer
from post.models import Follow, Likes, Post, Stream, Tag
from users_auth.models import Profile, User
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class Posts(APIView):
    def post(self, request, username):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(username=username)
            if user:
                profile = Profile.objects.get(user=user)
                # posts = Stream.objects.filter(user=user) 
                # post_ids = [post.post.id for post in posts]
                # post_items = Post.objects.filter(id__in=post_ids).order_by('-posted') 
                post_items = Post.objects.all().order_by('-posted') 


                response_data = []
                for post in post_items:
                    serializer = PostSerializer(post) 
                    post_data = serializer.data 
                    post_data['is_liked'] = Likes.objects.filter(user__id=user_id, post=post).exists()
                    post_data['is_faved'] = profile.favorites.filter(id=post.id).exists()
                    post_data['follow_status'] = Follow.objects.filter(following=post.user,follower__id=user_id).exists()
                    response_data.append(post_data)
                return Response(response_data, status=status.HTTP_200_OK)      
            else:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)      
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class NewPost(APIView):
    def post(self,request,username):
        try:
            user = User.objects.get(username=username)
            tags_objs = []
            if user:
                media_file = request.FILES.get('media_file')

                print(media_file)
                caption = request.data.get('caption')
                tags_form = request.data.get('tags')
                                 
                tags_list = list(tags_form.split(','))
                
                for tag in tags_list:
                    t,created = Tag.objects.get_or_create(title=tag)
                    tags_objs.append(t)
                p,created = Post.objects.get_or_create(media_file=media_file,caption=caption,user=user)  
                print("success")
                p.tags.set(tags_objs)
                p.save()
                return Response({"message":"post added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"User not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class TagPost(APIView):
    def get(self,request,title):
        print("hsjfhskajfdskfdkfsfa")
        try:
            tag = get_object_or_404(Tag,title=title)    
            posts = Post.objects.filter(tags=tag).order_by('-posted') 
            if posts:
                serializer = PostSerializer(posts, many=True)   
                print(serializer)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No Posts.'}, status=status.HTTP_404_NOT_FOUND)      
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class LikePost(APIView):
    def post(self,request,post_id):
        try:
            username = request.data.get('username')
            user = User.objects.get(username=username)
            if user: 
                post = Post.objects.get(id=post_id) 
                current_likes = post.likes  
                liked = Likes.objects.filter(user=user, post=post).count()  
                if not liked:
                    like = Likes.objects.create(user=user,post=post)
                    current_likes = current_likes + 1
                    like_serializer = LikesSerializer(like)
                else:
                    Likes.objects.filter(user=user, post=post).delete()
                    current_likes = current_likes - 1
                    like_serializer = None
                post.likes = current_likes
                post.save()  
                post_serializer = PostSerializer(post)
                return Response({
                'liked': bool(not liked),
                'post': post_serializer.data,
                'like': like_serializer.data if like_serializer else None
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error":"User not found"}, status=status.HTTP_400_BAD_REQUEST)    
        except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
                
                
                
                
                
class FavoritePost(APIView):
    def post(self, request, post_id):
        try:
            username = request.data.get('username')
            user = User.objects.get(username=username)
            if user: 
                post = Post.objects.get(id=post_id)
                profile = Profile.objects.get(user=user)
                if profile.favorites.filter(id=post_id).exists():
                    profile.favorites.remove(post)
                    message = "Post removed from favorites."
                else:
                    profile.favorites.add(post)
                    message = "Post added to favorites."
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
                     
        
            
        
        
            