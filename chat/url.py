from django.urls import path
from .views import chat_view
urlpatterns = [
    path('<str:room_name>/', chat_view, name='chat')
]
