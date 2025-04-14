from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "user_status"]
        error_messages = {
            'username': {
                'required': "Foydalanuvchi nomi majburiy.",
                'unique': "Bu foydalanuvchi nomi allaqachon mavjud.",
                'invalid': "Foydalanuvchi nomi noto'g'ri.",
                'max_length': "Foydalanuvchi nomi juda uzun.",
                'min_length': "Foydalanuvchi nomi juda qisqa.",
            },
            'email': {
                'required': "Email majburiy.",
                'invalid': "Email noto'g'ri.",
                'unique': "Bu email allaqachon mavjud.",
            },
            'password1': {
                'required': "Parol majburiy.",
                'password_too_short': "Parol juda qisqa.",
                'password_too_common': "Parol juda oddiy.",
                'password_entirely_numeric': "Parol faqat raqamlardan iborat bo'lishi mumkin emas.",
            },
            'password2': {
                'required': "Parolni tasdiqlash majburiy.",
                'password_mismatch': "Parollar mos kelmadi.",
            },
            'user_status': {
                'required': "Foydalanuvchi holati majburiy.",
            },
        }



