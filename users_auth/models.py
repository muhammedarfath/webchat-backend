from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.core.mail import message,send_mail
import uuid
from project import settings
import random

# Create your models here.



class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True,blank=True, null=True)
    otp = models.IntegerField(null= True,blank=True) 
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username   
    
def send_otp(sender, instance, created, **kwargs):
    if created:
        try:
            otp = str(random.randint(100000, 999999))
            instance.otp = otp
            instance.save()
            subject = "Your OTP for email verification"
            message = f"Hi, Your OTP is: {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.email]
            send_mail(subject, message, email_from, recipient_list)
        except Exception as e:
            print(e)
post_save.connect(send_otp, sender=User)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    date_of_birth = models.DateField(blank=True,null=True)  
    bio = models.CharField(max_length=300,blank=True, null=True)
    image = models.ImageField(upload_to='user_images', blank=True, null=True)


    def __str__(self):
        return self.user.username
    
def created_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
post_save.connect(created_user_profile,sender=User)      
