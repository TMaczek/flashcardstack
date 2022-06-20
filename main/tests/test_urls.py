from django.test import SimpleTestCase
from django.urls import reverse, resolve
import main.views as views
from django.contrib.auth import views as auth_views
from users import views as user_views

class TestUrls(SimpleTestCase):

    def test_homeUrlIsResolved(self):
        url = reverse('home') 
        self.assertEquals(resolve(url).func, views.home)

    def test_loginUrlIsResolved(self):
        url = reverse('login') 
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logoutUrlIsResolved(self):
        url = reverse('logout') 
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_registerUrlIsResolved(self):
        url = reverse('register') 
        self.assertEquals(resolve(url).func, user_views.register)

    def test_profileUrlIsResolved(self):
        url = reverse('profile') 
        self.assertEquals(resolve(url).func, user_views.profile)

    def test_addLessonUrlIsResolved(self):
        url = reverse('addlesson') 
        self.assertEquals(resolve(url).func, views.addLesson)

    def test_addCardUrlIsResolved(self):
        url = reverse('addcard') 
        self.assertEquals(resolve(url).func, views.addCard)

    def test_showCardUrlIsResolved(self):
        url = reverse('showcards') 
        self.assertEquals(resolve(url).func, views.showCards)

    def test_correctUrlIsResolved(self):
        url = reverse('correct') 
        self.assertEquals(resolve(url).func, views.correct)

    def test_incorrectUrlIsResolved(self):
        url = reverse('incorrect') 
        self.assertEquals(resolve(url).func, views.incorrect)

    def test_loadcardsUrlIsResolved(self):
        url = reverse('loadcards', args=[1]) 
        self.assertEquals(resolve(url).func, views.loadCards)

    def test_editLessonUrlIsResolved(self):
        url = reverse('editlesson') 
        self.assertEquals(resolve(url).func, views.editLesson)

    def test_editCardsUrlIsResolved(self):
        url = reverse('editcards', args=[1]) 
        self.assertEquals(resolve(url).func, views.editCards)

    def test_deleteLessonUrlIsResolved(self):
        url = reverse('deletelesson', args=[1]) 
        self.assertEquals(resolve(url).func, views.deleteLesson)

    def test_deleteCardUrlIsResolved(self):
        url = reverse('deletecard', args=[1]) 
        self.assertEquals(resolve(url).func, views.deleteCard)