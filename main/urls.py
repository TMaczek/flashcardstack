from django.urls import path
from users import views as user_views
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', user_views.register, name = 'register'),
    path('login/', user_views.login, name = 'login')
]