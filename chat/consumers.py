import json
from channels.generic.websocket import AsyncWebsocketConsumer
# To'g'ri User modelini import qilish
# from django.contrib.auth.models import User # <<< O'chirilsin
from register.models import CustomUser # <<< Qo'shilsin
from .models import Message
from channels.db import database_sync_to_async # <<< Qo'shilsin
from django.shortcuts import get_object_or_404 # <<< Qulaylik uchun qo'shilishi mumkin

class ChatConsumer(AsyncWebsocketConsumer):

    # --- database_sync_to_async yordamchi funksiyalari ---
    @database_sync_to_async
    def get_user(self, username):
        # get_object_or_404 ni ishlatsa ham bo'ladi, lekin u sinxron
        # Shuning uchun try-except yoki filter().first() yaxshiroq
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None # Yoki xatolik qaytarish

    @database_sync_to_async
    def create_message(self, sender, receiver, content):
        return Message.objects.create(sender=sender, receiver=receiver, content=content)
    # --- ---

    async def connect(self):
        print("ws ulanishga harakat...")
        self.user = self.scope["user"]

        # Foydalanuvchi autentifikatsiyadan o'tganligini tekshirish
        if not self.user or not self.user.is_authenticated:
            print("Autentifikatsiyadan o'tmagan foydalanuvchi. Ulanish rad etildi.")
            await self.close()
            return

        self.other_username = self.scope["url_route"]["kwargs"]["username"]
        self.other_user = await self.get_user(self.other_username)

        if not self.other_user:
            print(f"Foydalanuvchi '{self.other_username}' topilmadi. Ulanish rad etildi.")
            await self.close()
            return

        # ID'lar orqali xona nomini yaratish (tartiblangan holda)
        # Foydalanuvchi o'zi bilan chat qila olmasligini ham tekshirish mumkin
        if self.user.id == self.other_user.id:
             print("Foydalanuvchi o'zi bilan chat qila olmaydi. Ulanish rad etildi.")
             await self.close()
             return

        # Xona nomini yaratish (ID'larni tartiblash orqali)
        user_ids = sorted([self.user.id, self.other_user.id])
        self.room_name = f"chat_{user_ids[0]}_{user_ids[1]}"
        self.room_group_name = self.room_name # Odatda room_name bilan bir xil bo'ladi

        print(f"'{self.user.username}' uchun '{self.room_group_name}' guruhiga qo'shilish...")

        # Guruhga qo'shilish
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Ulanishni qabul qilish
        await self.accept()
        print(f"'{self.user.username}' WS ga muvaffaqiyatli ulandi.")

    async def disconnect(self, close_code):
        print(f"'{self.user.username}' WS dan uzildi (code: {close_code})")
        # Guruhdan chiqish (agar room_group_name mavjud bo'lsa)
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        print(f"'{self.user.username}' dan xabar qabul qilindi: {text_data}")
        try:
            data = json.loads(text_data)
            message_content = data.get("message")

            if not message_content:
                print("Xabarda 'message' maydoni yo'q.")
                return

            # Xabarni DB ga asinxron saqlash
            sender = self.user
            # other_user connect metodida olingan, qayta qidirish shart emas
            receiver = self.other_user

            # Agar other_user connectda topilmagan bo'lsa (ehtimoldan yiroq, lekin tekshirish mumkin)
            if not receiver:
                 print("Qabul qiluvchi topilmadi (receive).")
                 return

            msg = await self.create_message(sender=sender, receiver=receiver, content=message_content)
            print(f"Xabar DB ga saqlandi: {msg.id}")

            # Xabarni guruhga yuborish
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message", # Bu quyidagi chat_message metodini chaqiradi
                    "message": message_content,
                    "sender": sender.username,
                    # Yana qo'shimcha ma'lumotlar yuborish mumkin, masalan timestamp
                    "timestamp": msg.timestamp.isoformat(),
                }
            )
            print(f"Xabar '{self.room_group_name}' guruhiga yuborildi.")

        except json.JSONDecodeError:
            print("Xato: Qabul qilingan ma'lumot JSON formatida emas.")
        except Exception as e:
            print(f"Xabar qabul qilishda xatolik: {e}")


    # Guruhdan xabar kelganda chaqiriladi
    async def chat_message(self, event):
        print(f"'{self.user.username}' ga xabar yuborilmoqda: {event}")
        message = event["message"]
        sender = event["sender"]
        timestamp = event.get("timestamp") # Timestampni ham olish

        # WebSocket orqali klientga xabarni yuborish
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "timestamp": timestamp, # Klientga ham yuborish
        }))
        print("Xabar klientga yuborildi.")

