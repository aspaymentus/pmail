from databaselayer.connection import dbConnection
from databaselayer import queries
from django import forms


class UserEmailForm(forms.Form):
    receiverEmail = forms.EmailField(label = "Email")
    subject = forms.CharField(label = "Subject" , max_length=200)
    text = forms.CharField(label = "Body" , widget=forms.TextInput())

    def saveEmail(self,findFilter,data):
        myCollection = dbConnection('Pmail','inbox')
        queries.saveEmailQuery(myCollection,findFilter,data)



