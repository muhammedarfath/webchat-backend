from django.urls import path
from .views import LastThreeMessages

urlpatterns = [
    path('last-three-messages/<int:userId>/', LastThreeMessages.as_view(), name='last_three_messages'),
]
