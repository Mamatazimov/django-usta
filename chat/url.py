from django.urls import path
from .views import chat_view
urlpatterns = [
    path('<str:username>/', chat_view, name='chat')
]