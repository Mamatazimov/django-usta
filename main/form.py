from .models import Profile, Post, MastersCategory
from django import forms
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'id':'imageUpload'}),required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Bio','class':'myinput'}),required=False)
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Age','class':'myinput'}),required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Phone Number','class':'myinput'}),required=False)
    telegram_link = forms.URLField(widget=forms.URLInput(attrs={'placeholder':'Telegram Link','class':'myinput'}),required=False)
    instagram_link = forms.URLField(widget=forms.URLInput(attrs={'placeholder':'Instagram Link','class':'myinput'}),required=False)
    class Meta:
        model = Profile
        fields = ['bio','avatar','age','phone_number','telegram_link','instagram_link']

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name','class':'myinput'}),required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name','class':'myinput'}),required=False)
    class Meta:
        model = User
        fields = ['first_name','last_name']

class PostForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput(attrs={'id':'postPhoto'}), required=False)
    body = forms.CharField(widget=forms.Textarea(attrs={'id':'postBody','placeholder':'Sharh...'}),required=False)
    class Meta:
        model = Post
        fields = ['photo','body']

class CategoryForm(forms.Form):
    selected_option = forms.ModelChoiceField(
        queryset=MastersCategory.objects.all(),
        empty_label=None,
        required=False,
        label="Mahorat"
    )