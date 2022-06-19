
from http import client
from django.test import TestCase, Client
from django.urls import reverse
import users.views as views
import json
from django.contrib.auth import get_user_model, get_user, authenticate
# Create your tests here.

class testUserViews(TestCase):

    def setUp(self):
        self.client = Client()

    def loginUserForTests(self):
        User = get_user_model()
        self.client = Client()
        self.username='testuser'
        self.email = 'test@test.com'
        self.password='12345'
        self.user = User(username=self.username,email=self.email)
        self.user.set_password(self.password)
        self.user.save() 
        login = self.client.login(username=self.username,password=self.password)
        self.assertEqual(login,True)

    def test_profile(self):
        self.loginUserForTests()
        response = self.client.get(reverse('profile'))

        self.assertEquals(response.status_code, 200)
        assert 'users/profile.html' in (t.name for t in response.templates) 

    def test_register(self):
        self.loginUserForTests()
        response = self.client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        assert 'users/register.html' in (t.name for t in response.templates) 