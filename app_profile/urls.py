from django.urls import path
from .views import UserProfile

urlpatterns = [
   path('userprofile/',UserProfile.as_view(),name='userprofile')
]
