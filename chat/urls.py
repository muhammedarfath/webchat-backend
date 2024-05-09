from django.urls import path
from .views import index,LoginView,room
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", index, name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("<str:room_name>/", room, name="room"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]