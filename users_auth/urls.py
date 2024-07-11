from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import LoginView, SignUpView,OTPVerificationView,ResentOTP





urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('verify-otp/',OTPVerificationView.as_view(),name='verify-otp'),
    path('resend-otp/',ResentOTP.as_view(),name='resend-otp'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]    



