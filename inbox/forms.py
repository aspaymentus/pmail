from django import forms
from celery import shared_task

class UserEmailForm(forms.Form):
    receiverEmail = forms.EmailField(label = "Email")
    subject = forms.CharField(label = "Subject" , max_length=200)
    text = forms.CharField(label = "Body" , widget=forms.TextInput())



