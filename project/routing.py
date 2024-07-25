# project/routing.py
from django.urls import re_path, path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('chat/',ChatConsumer.as_asgi())
]






