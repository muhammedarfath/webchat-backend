from django.urls import path
from .views import RoomView,Users,Suggested,FriendUser

urlpatterns = [
    path("users/", Users.as_view(), name="users"),
    path("frienduser/", FriendUser.as_view(), name="frienduser"),
    path("suggested_friends/", Suggested.as_view(), name="suggested_friends"),
    path("<str:room_name>/",  RoomView.as_view(), name='room_view'),
]
