from django import forms
from django.contrib.auth.models import User




class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=100 , widget=forms.TextInput(attrs={'class': "form__input"}))
    login = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    

    class Meta:
        model = User
        fields = ['username', 'login', 'password']