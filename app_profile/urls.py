from django.urls import path
from .views import UserProfile,FollowRequest,FollowBackRequest,CheckRelationship

urlpatterns = [
   path('userprofile/',UserProfile.as_view(),name='userprofile'),
   path("send_follow_request/", FollowRequest.as_view(), name="send_follow_request"),  
   path("follow_back_request/", FollowBackRequest.as_view(), name="follow_back_request"),  
   path("check_relationship/", CheckRelationship.as_view(), name="check_relationship"),  

]
