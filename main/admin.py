from django.contrib import admin

# Register your models here.

from .models import Profile, Post, MastersCategory

admin.site.register(MastersCategory)