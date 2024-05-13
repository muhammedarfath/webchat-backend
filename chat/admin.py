from django.contrib import admin

from .models import Profile,User,Message

# Register your models here.

class ChatMessage(admin.ModelAdmin):
    list_display = ['author','recipient','content','timestamp']
    
    
admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Message,ChatMessage)
