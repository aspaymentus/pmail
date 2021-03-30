from django import forms
from databaselayer.connection import dbConnection
from databaselayer import queries
from django.contrib.auth import password_validation
from .validators import validatorEmail,validatorUsername
from django.utils.translation import ugettext,ugettext_lazy as _

class UserRegisterForm(forms.Form):
    username = forms.CharField(label = "Username" , max_length=40,help_text='Must be unique',validators=[validatorUsername])
    email = forms.EmailField(help_text="Please enter a valid email address",validators=[validatorEmail])
    password = forms.CharField(label=_('Password') , widget= forms.PasswordInput,help_text=password_validation.password_validators_help_text_html())
    
  
    def saveData(self,data):
        myCollection = dbConnection('Pmail' , 'user_data')
        queries.insertQuery(myCollection , data)


class UserLoginForm(forms.Form):
    username = username = forms.CharField(label = "Username" , max_length=40)
    password = forms.CharField(label=_('Password') , widget= forms.PasswordInput)