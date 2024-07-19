# urls.py
from django.urls import path
from .views import Posts,NewPost,TagPost,LikePost,FavoritePost,AddComment

urlpatterns = [
    path('posts/<str:username>/', Posts.as_view(), name='user-posts'),
    path('add-post/<str:username>/', NewPost.as_view(), name='add-post'),
    path('tag-post/<str:title>/', TagPost.as_view(), name='tag-post'),
    path('like-post/<int:post_id>/', LikePost.as_view(), name='tlike-post'),
    path('fav-post/<int:post_id>/', FavoritePost.as_view(), name='fav-post'),
    path('comment-post/<str:username>/', AddComment.as_view(), name='comment-post'),
]
