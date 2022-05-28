from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views
from main import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name = 'logout'),
    path('register/', user_views.register, name = 'register'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/addlesson', views.addLesson, name='addlesson'),
    path('profile/addcard/', views.addCard, name='addcard'),
    path('profile/showcards/<int:lesson>', views.showCards, name='showcards')
]