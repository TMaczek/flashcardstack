from django import forms
from django.forms.widgets import NumberInput

class AddCardForm(forms.Form):
    front_text = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': "form__input"}),max_length=100)
    back_text = forms.CharField(label="Definition", widget=forms.TextInput(attrs={'class': "form__input"}),max_length=100)
    
class AddLessonForm(forms.Form):
    title = forms.CharField(label = "Title", widget=forms.TextInput(attrs={'class': "form__input"}),max_length=100)
    description = forms.CharField(label = "Description",widget=forms.TextInput(attrs={'class': "form__input"}),max_length=100)