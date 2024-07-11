from django.contrib import admin

from .models import Message,Notification

# Register your models here.

class ChatMessage(admin.ModelAdmin):
    list_display = ['author','recipient','content','timestamp']
    
    

admin.site.register(Notification)
admin.site.register(Message,ChatMessage)
