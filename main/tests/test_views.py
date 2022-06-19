from http import client
from django.test import TestCase, Client
from django.urls import reverse
import main.views as views
import json
from django.contrib.auth import get_user_model, get_user, authenticate
from flashcardstack.models import Lesson, FlashCard
# Create your tests here.

class testMainViews(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

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

    def test_homeNoLoggin(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_homeLoggin(self):
        self.loginUserForTests() 
        response = self.client.get(reverse('home'))

        self.assertRedirects(response, '/profile/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_addCardNotLoggedIn(self):
        response = self.client.get(reverse('addcard'))

        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_addCardLoggedIn(self):
        self.loginUserForTests() 
        response = self.client.get(reverse('addcard'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/addcard.html')

    def test_addLessonNotLoggedIn(self):
        response = self.client.get(reverse('addlesson'))

        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_addLessonLoggedIn(self):
        self.loginUserForTests() 
        response = self.client.get(reverse('addlesson'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/addlesson.html')

    def test_loadCards(self):
        response = self.client.get(reverse('loadcards', args=[1]))
        self.assertEquals(len(views.currentFlashcards), 1)
        self.assertRedirects(response, '/profile/showcards', status_code=302, target_status_code=200, fetch_redirect_response=False)

    def test_showCardsProfileRedirect(self):
        response = self.client.get(reverse('loadcards', args=[1]))
        response = self.client.get(reverse('showcards'))

        self.assertRedirects(response, '/profile/', status_code=302, target_status_code=200, fetch_redirect_response=False)

    def test_editLesson(self):
        self.loginUserForTests() 
        response = self.client.get(reverse('editlesson'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/editlesson.html')

    def test_editCards(self):
        self.loginUserForTests() 
        response = self.client.get(reverse('editcards', args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/editcards.html')