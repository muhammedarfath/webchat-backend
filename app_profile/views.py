from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from users_auth.models import User
from post.serializers import PostSerializer
from post.models import Follow, Post
from users_auth.serializers import ProfileSerializer, UserDetailsSerializer
from chat.models import Profile
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.


class UserProfile(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_name = request.data.get('username')
        current_user = request.data.get('current_user')
        
        try:
            if user_name:
                profile = Profile.objects.get(user__username=user_name)
                posts = Post.objects.filter(user__username=user_name).order_by("-posted")
                profile_serializer = UserDetailsSerializer(profile)
                post_serializer = PostSerializer(posts,many=True)
                
                #check follow status
                follow_status = Follow.objects.filter(following__username=user_name,follower__username=current_user).exists()
                
                
                response_data = {
                    "profile": profile_serializer.data,
                    "posts": post_serializer.data,
                    "follow_status":follow_status
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowRequest(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        current_user_id = request.data.get('current_user')
        friend_user_username = request.data.get('follow_user')

        if current_user_id is not None and friend_user_username is not None:
            try:
                following = get_object_or_404(User, username=friend_user_username)
                follow_user = Follow.objects.filter(follower=current_user_id, following=following)
                friend_user = Follow.objects.filter(follower=following, following=current_user_id)
                if follow_user.exists() and friend_user.exists():
                    follow_user.delete()
                    return Response({"message": "User Already following"}, status=status.HTTP_200_OK)
                elif follow_user.exists():
                    follow_user.delete()
                    return Response({"message": "Unfollowed successfully"}, status=status.HTTP_200_OK)
                else:
                    Follow.objects.create(follower_id=current_user_id, following=following)
                    return Response({"message": "Follow request sent"}, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:  
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Both current_user and follow_user are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class FollowBackRequest(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        current_user_id = request.data.get('current_user')
        follow_user_username = request.data.get('follow_user')

        if current_user_id is not None and follow_user_username is not None:
            try:
                current_user = get_object_or_404(User, id=current_user_id)
                follow_user = get_object_or_404(User, username=follow_user_username)

                follow_relationship = Follow.objects.filter(follower=current_user, following=follow_user)

                if follow_relationship.exists():
                    return Response({'message': 'Already following'}, status=status.HTTP_200_OK)
                else:
                    Follow.objects.create(follower=current_user, following=follow_user)
                    return Response({'message': 'Followed back successfully'}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Both current_user and follow_user are required'}, status=status.HTTP_400_BAD_REQUEST)   
        
             
        
class CheckRelationship(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        current_user_id = request.query_params.get('current_userId')
        follow_user_username = request.query_params.get('follow_user')

        if current_user_id is not None and follow_user_username is not None:
            try:
                current_user = get_object_or_404(User, id=current_user_id)
                follow_user = get_object_or_404(User, username=follow_user_username)

                if current_user == follow_user:
                    return Response({'status': 'self'}, status=status.HTTP_200_OK)

                follows = Follow.objects.filter(follower=current_user, following=follow_user).exists()
                followed_by = Follow.objects.filter(follower=follow_user, following=current_user).exists()

                if follows and followed_by:
                    return Response({'status': 'followed'}, status=status.HTTP_200_OK)
                elif follows:
                    return Response({'status': 'following'}, status=status.HTTP_200_OK)
                elif followed_by:
                    return Response({'status': 'followback'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'none'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Both currentUserId and followUserId are required'}, status=status.HTTP_400_BAD_REQUEST)        