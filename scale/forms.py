from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('username', 'password1', 'password2',)
        widgets = {
            'username': forms.TextInput(attrs={'class': ''}),
            'password1': forms.PasswordInput(attrs={'class': ''}),
            'password2': forms.PasswordInput(attrs={'class': ''})
        }
