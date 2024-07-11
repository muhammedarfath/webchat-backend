from django.db import models
from django.db.models import Q
from django.core.validators import RegexValidator
from users_auth.models import User,Profile

# Create your models here.
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    
    @classmethod
    def notification_for_room(cls, user_id):
        return cls.objects.filter(
            user_id=user_id
        ).order_by('timestamp')[:100]


class Message(models.Model):
    author = models.ForeignKey(User,related_name='sent_messages',on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages',null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.author.username
    
    @classmethod
    def messages_for_room(cls, author_id, recipient_profile_id):
        return cls.objects.filter(
            Q(author_id=author_id, recipient_id=recipient_profile_id) |
            Q(author_id=recipient_profile_id, recipient__user_id=author_id)
        ).order_by('timestamp')[:100]
    
