from django.urls import path
from .views import RoomView,Users,EditProfile,Suggested,FollowRequest

urlpatterns = [
    path("users/", Users.as_view(), name="users"),
    path("suggested_friends/", Suggested.as_view(), name="suggested_friends"),
    path("send_follow_request/", FollowRequest.as_view(), name="send_follow_request"),  
    path("<str:room_name>/",  RoomView.as_view(), name='room_view'),
    path('edit/<int:id>/',EditProfile.as_view(),name='edit'),
]
