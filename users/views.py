from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import views as auth_views
from flashcardstack.models import Lesson


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'{username} Created succesfuly')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form':form})


# def login(request):
#     if request.user.is_authenticated:
#         return redirect('profile')
#     return redirect(auth_views.LoginView.as_view(template_name='users/login.html'))

@login_required
def profile(request):
    request.session["lesson_id"]=None
    lessons = Lesson.objects.filter(user = request.user)
    return render(request, 'users/profile.html', {'lessons':lessons})
