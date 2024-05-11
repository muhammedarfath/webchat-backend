from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db import models

# Create your models here.



class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(unique=True)
    
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    bio = models.CharField(max_length=300)
    image = models.ImageField(upload_to='user_images', blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    



class Message(models.Model):
    author = models.ForeignKey(User,related_name='author_messages',on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.author.username
    
    def last_10_messages():
        return Message.objects.order_by('timestamp').all()[:100]
    
    
    
def created_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    
    
post_save.connect(created_user_profile,sender=User)      