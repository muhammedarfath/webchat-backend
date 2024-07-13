# project/routing.py
from django.urls import re_path, path
from chat.consumers import ChatConsumer,NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', NotificationConsumer.as_asgi()),
]






