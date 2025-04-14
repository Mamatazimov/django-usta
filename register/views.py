from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy

from .form import CustomUserCreationForm



class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "register.html"



class LoginView(AuthLoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy("dashboard")
