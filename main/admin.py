from django.contrib import admin

# Register your models here.

from .models import Profile, Post, MatersCategory

admin.site.register(MatersCategory)