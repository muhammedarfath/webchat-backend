from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import LogoutView,LoginView, SignUpView,OTPVerificationView,ResentOTP,ResetPassword,PasswordResetConfirm,EditProfile


app_name="users_auth"


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('verify-otp/',OTPVerificationView.as_view(),name='verify-otp'),
    path('resend-otp/',ResentOTP.as_view(),name='resend-otp'),
    path('edit/<int:id>/',EditProfile.as_view(),name='edit'),
    path('reset-password/',ResetPassword.as_view(),name='reset-password'),
    path('password-reset-confirm/<int:user_id>/',PasswordResetConfirm.as_view(),name='password-reset-confirm'),
    path('token/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),name ='token_refresh')
]
     
     