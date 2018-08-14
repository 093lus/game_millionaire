from django.contrib.auth.models import User
from django.forms import forms
from django.forms import ModelForm, CharField, PasswordInput


class UserForm(ModelForm):
    username = CharField(help_text="Please enter a username.")
    email = CharField(help_text="Please enter your email.")
    password = CharField(widget=PasswordInput(), help_text="Please enter your password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
