# urls.py
from django.urls import path
from .views import Posts,NewPost,TagPost

urlpatterns = [
    path('posts/<str:username>/', Posts.as_view(), name='user-posts'),
    path('add-post/<str:username>/', NewPost.as_view(), name='add-post'),
    path('tag-post/<str:title>/', TagPost.as_view(), name='tag-post'),
]
