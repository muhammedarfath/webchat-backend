from django.urls import path
from .views import GetNews

urlpatterns = [
    path("<str:topic>/",GetNews.as_view(), name='get-news'),
]
