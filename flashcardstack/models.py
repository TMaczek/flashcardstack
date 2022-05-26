from django.db import models
from django.contrib.auth.models import User

class FlashCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    date_of_last_notice = models.DateField(auto_now=True)
    notice_lvl_in_days = models.DecimalField(decimal_places=0, max_digits=5)
    content = models.TextField()

    def __str__(self):
        return self.content