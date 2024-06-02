from django.urls import path
from .views import LoginView,RoomView,Users,SignUpView,EditProfile,Suggested
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("users/", Users.as_view(), name="users"),
    path("suggested_friends/", Suggested.as_view(), name="suggested_friends"),
    path("login/", LoginView.as_view(), name="login"),
    path('signup/',SignUpView.as_view(),name='signup'),
    path("<str:room_name>/",  RoomView.as_view(), name='room_view'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('edit/<int:id>/',EditProfile.as_view(),name='edit'),

]