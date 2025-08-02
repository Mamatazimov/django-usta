import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message
from asgiref.sync import sync_to_async
from register.models import CustomUser
from django.db.models import Q
from .models import Message

@sync_to_async
def get_user(username):
    return CustomUser.objects.filter(username=username).first()

@sync_to_async
def add_message(room_name,sender,receiver,content):
    msg = Message(room_name=room_name,sender=sender,receiver=receiver,content=content)
    msg.save()

@sync_to_async
def get_message(room_name=None,sender=None,receiver=None,user=None):
    if room_name is not None:
        return Message.objects.filter(room_name=room_name)
    
    if sender is not None:
        return Message.objects.filter(sender=sender)

    if receiver is not None:
        return Message.objects.filter(receiver=receiver)

    if user is not None:
        return Message.objects.filter(Q(sender=user)|Q(receiver=user))

    return Message.objects.all()
     

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]
        print(self.user,self.user.username)
        
        if len(str(self.room_name).split("-")) != 2:
            return await self.close()

        usr1,usr2=str(self.room_name).split("-")
        if self.user.username not in [usr1,usr2]:
            return await self.close()

        usr1 = await get_user(usr1)
        usr2 = await get_user(usr2)

        if usr1 is None or usr2 is None:
            return await self.close()

        if usr1.username == self.user.username:
            self.sender = usr1
            self.receiver = usr2
        else:
            self.receiver = usr1
            self.sender = usr2

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        print(data)
        await add_message(room_name=self.room_name,sender=self.sender,receiver=self.receiver,content=message) 
        

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                "username": username
                
            }
        )


    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        

        
        await self.send(text_data=json.dumps({
            'message': message,
            'username':username
        }))
