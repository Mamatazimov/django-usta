from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=120, null=False)
    password = models.CharField(max_length=320)
    email = models.EmailField(unique=True)
    simpleUser = models.BooleanField(default=True)
    

