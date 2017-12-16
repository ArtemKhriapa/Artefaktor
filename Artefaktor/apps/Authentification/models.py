from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
# Create your models here.
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=500, help_text='Required')
#as far as UserCreationForm was imported
#we can do a sign up form with extra field email
# https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class Authorization(AuthenticationForm):
    pass