from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
import os
import requests

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

class GetNews(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, topic):
        cache_key = f'news_{topic}'
        try:
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data, status=status.HTTP_200_OK)
            
            url = f"{BASE_URL}&topic={topic}&token={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            cache.set(cache_key, data, timeout=86400)
            return Response(data, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to fetch news: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
