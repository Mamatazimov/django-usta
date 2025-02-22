from django import forms
from django.core.exceptions import ValidationError

from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(email)
        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu email allaqachon ishlatilgan.")
        return email
        
    class Meta:
        model = User
        fields = ['name', 'password','email','simpleUser']