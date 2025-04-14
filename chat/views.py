from django.shortcuts import render, get_object_or_404
from register.models import CustomUser

def chat_view(request, username):
    other_user = get_object_or_404(CustomUser, username=username)
    return render(request, "chat.html", {"other_user": other_user})
