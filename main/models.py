from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(blank=True,null=True)
    avatar = models.ImageField(upload_to="avatars/",default="avatars/default.png",blank=True,null=True)
    age = models.PositiveIntegerField(default=0,blank=True,null=True)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    telegram_link = models.URLField(blank=True,null=True)   
    instagram_link = models.URLField(blank=True,null=True)
    m_category = models.ForeignKey('MastersCategory', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="posts/",blank=True)
    body = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.user.username
    
class MastersCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
