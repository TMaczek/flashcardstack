from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title

class FlashCard(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    date_of_last_notice = models.DateField(auto_now=True)
    notice_lvl_in_days = models.IntegerField()
    front_text = models.TextField()
    back_text = models.TextField()

    def __str__(self):
        return self.front_text+";"+self.back_text

