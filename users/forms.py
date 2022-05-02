from django import forms
from django.contrib.auth.models import User




class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    login = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    

    class Meta:
        model = User
        fields = ['username', 'login', 'password']