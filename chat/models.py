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
    


def created_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    
    
post_save.connect(created_user_profile,sender=User)    


class Message(models.Model):
    author = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    sender = models.ForeignKey(User,related_name='sender',on_delete=models.CASCADE,blank=True, null=True)
    reciever = models.ForeignKey(User,related_name='receiver',on_delete=models.CASCADE,blank=True, null=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False,blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        verbose_name_plural = 'Message'
    
    def __str__(self):
        return f"{self.sender} - {self.receiver}"
    
    @property
    def sender_profile(self):
        sender_profile = Profile.objects.get(user=self.sender)
        return sender_profile
    
    @property
    def receiver_profile(self):
        receiver_profile = Profile.objects.get(user=self.receiver)
        return receiver_profile
    
    
  