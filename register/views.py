from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import User
from .form import UserForm


class UserRegisterView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'register.html'
    success_url = reverse_lazy('register') 

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data["password"])
        user = form.save()
        return super().form_valid(form) 


