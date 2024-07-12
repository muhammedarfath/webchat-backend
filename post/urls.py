# urls.py
from django.urls import path
from .views import Posts

urlpatterns = [
    path('posts/<str:username>/', Posts.as_view(), name='user-posts'),
]
