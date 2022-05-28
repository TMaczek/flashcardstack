from django import forms
from django.forms.widgets import NumberInput

class AddCardForm(forms.Form):
    front_text = forms.CharField(label="front_text", max_length=200)
    back_text = forms.CharField(label="back_text", max_length=200)
    
class AddLessonForm(forms.Form):
    title = forms.CharField(label = "Title", max_length=50)
    description = forms.CharField(label = "Description", max_length=200)