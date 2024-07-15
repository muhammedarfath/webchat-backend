from django.urls import path
from .views import RoomView,Users,Suggested

urlpatterns = [
    path("users/", Users.as_view(), name="users"),
    path("suggested_friends/", Suggested.as_view(), name="suggested_friends"),
    path("<str:room_name>/",  RoomView.as_view(), name='room_view'),
]
