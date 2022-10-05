from distutils.command.upload import upload
from email.mime import image
from email.policy import default
from pyexpat import model
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField(null=True)
      
    def __str__(self):
       return self.name

class Category(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
       return self.name
       
    def get_absolute_url(self):
        return reverse('home')

class Post(models.Model):
    title = models.CharField(max_length=100,null=True)
    username = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    body = RichTextUploadingField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = "images/",null=True,blank=True,default='images/default.png')
    snippet = models.CharField(max_length=255,default='Click Link Above To Read Blog Post...')
    likes = models.ManyToManyField(User,related_name='blog_post')
    category=models.CharField(max_length=255,default='uncategorised')


    class Meta:
        ordering=['-date']

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
       return self.title + ' | ' +str(self.username)
       
    def get_absolute_url(self):
        return reverse('home')

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name="comments", on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=255)
    body=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return '%s - %s' %(self.post.title, self.name)
    
    class Meta:
        ordering = ('-date_added',)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    pic=models.ImageField(default='images/user.webp',upload_to = "pics/")
    bio=models.TextField(null=True,blank=True)
    website_url=models.CharField(max_length=255,null=True,blank=True)
    fb_url=models.CharField(max_length=255,null=True,blank=True)
    twitter_url=models.CharField(max_length=255,null=True,blank=True)
    instagram_url=models.CharField(max_length=255,null=True,blank=True)
    linkedin_url=models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
       return str(self.user)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
