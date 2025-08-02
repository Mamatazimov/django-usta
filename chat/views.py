from django.shortcuts import render, get_object_or_404
from register.models import CustomUser
from .models import Message

def chat_view(request, room_name):
    room_messages = Message.objects.filter(room_name=room_name)
    other = list(set(room_name.split("-")) ^ set([request.user.username]))[0]
    return render(request, "chat.html",{"room":room_name,"username":request.user.username,"room_messages":room_messages,"other":other})
