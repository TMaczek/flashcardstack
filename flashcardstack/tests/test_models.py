from django.test import TestCase, Client
from flashcardstack.models import FlashCard, Lesson
from django.contrib.auth import get_user_model, get_user, authenticate

class TestModels(TestCase):

    def setUp(self):
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
        self.lesson = Lesson(user = self.user,
                            title = 'testTitle',
                            description = 'testDescription' 
                            )
        self.flashCard = FlashCard(
                        lesson = self.lesson,
                        notice_lvl_in_days = 1,
                        front_text = 'testFrontText',
                        back_text = 'testBackText'
                    )


    def test_LessonToString(self):
        self.assertEqual(str(self.lesson), "testTitle")

    def test_FlashCardToString(self):
        self.assertEqual(str(self.flashCard), "testFrontText" + ";" + "testBackText")