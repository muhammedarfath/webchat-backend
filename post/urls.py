# urls.py
from django.urls import path
from .views import Posts,NewPost

urlpatterns = [
    path('posts/<str:username>/', Posts.as_view(), name='user-posts'),
    path('add-post/<str:username>/', NewPost.as_view(), name='add-post'),
]
