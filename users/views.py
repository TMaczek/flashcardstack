from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import views as auth_views
from flashcardstack.models import Lesson
from main.views import clearCurrentFlashcards


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


@login_required
def profile(request):
    clearCurrentFlashcards(request)
    request.session["lesson_id"]=None
    lessons = Lesson.objects.filter(user = request.user)
    return render(request, 'users/profile.html', {'lessons':lessons})
