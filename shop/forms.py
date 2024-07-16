from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Customer


class LoginRegister(UserCreationForm):
    username = forms.CharField(label="username")
    password1 = forms.CharField(label="mobile", widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('username', 'password1',)
