from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
import sys
sys.path.append("..")
from flashcardstack.database import connection



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            DC = connection.DatabaseConnection()
            DC.addUser(username, login, password)
            messages.success(request, f'{username} Created succesfuly {login}, {password}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})


def login(request):
    return render(request, 'users/login.html')

