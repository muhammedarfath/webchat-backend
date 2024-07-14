from typing import Iterable
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save

# Create your models here.
def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class Tag(models.Model):
    title = models.CharField(max_length=75,verbose_name='Tag')
    slug = models.SlugField(null=True,unique=True)
    
    class Meta:
        verbose_name_plural = 'Tags'
        
    # def get_absolute_url(self):
    #     return reverse("tags", args=[self.slug])
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args,**kwargs)    
         

class Post(models.Model):
    picture = models.ImageField(upload_to=user_directory_path,verbose_name='Picture',null=False)
    caption = models.TextField(max_length=1500,verbose_name="Caption")
    posted = models.DateTimeField(auto_now_add = True)
    tags = models.ManyToManyField(Tag,related_name='tags')
    user = models.ForeignKey('users_auth.User', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse("postdetails", args={str(self.id)})
    
class Follow(models.Model):
    follower = models.ForeignKey('users_auth.User',on_delete=models.CASCADE,related_name="follower")   
    following = models.ForeignKey('users_auth.User',on_delete=models.CASCADE,related_name="following")   
    
class Stream(models.Model):
    following = models.ForeignKey('users_auth.User',on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey('users_auth.User',on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date = models.DateTimeField()
    
    def add_post(sender,instance,*args,**kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post,user=follower.follower,date=post.posted,following=user)
            stream.save()
            
post_save.connect(Stream.add_post,sender=Post)     



class Likes(models.Model):
	user = models.ForeignKey('users_auth.User', on_delete=models.CASCADE, related_name='user_like')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')    

    
    
    