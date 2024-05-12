from django.contrib import admin

from .models import Profile,User,Message

# Register your models here.

class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['sender','receiver','content','is_read']

admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Message,ChatMessageAdmin)
