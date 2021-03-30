from django.shortcuts import render,redirect
from django.http import HttpResponse
# from databaselayer.connection import dbConnection
# from databaselayer import queries
from .forms import UserEmailForm
from django.contrib import messages
from databaselayer import *
# Create your views here.

def home(request):
    return render( request , 'inbox/base.html')

def loginRedirect(request):
    return render(request,'inbox/loginView.html')

def inbox(request):
    myCollection = connection.dbConnection('Pmail' , 'user_data')
    username = queries.findWithProjectionQuery(myCollection,{'is_login' : True} , {'username' : 1})['username']
    myCollection = connection.dbConnection('Pmail' , 'inbox')
    data = queries.findWithProjectionQuery(myCollection , {'username' : username} , {'messages' : 1})
    return render(request , 'inbox/inbox_view.html',context = {'mails' : data['messages']})

def compose(request):
    if request.method=='POST':
        form = UserEmailForm(request.POST)
        if form.is_valid():
            myCollection = connection.dbConnection('Pmail' , 'user_data')
            activeUser = queries.findWithProjectionQuery(myCollection , {'is_login' : True} , {'username' : 1 , 'email' : 1} )
            
            data = {
                "senderName" : activeUser['username'],
                "senderEmail" : activeUser['email'],
                "subject" : form.cleaned_data.get('subject'),
                "message" : form.cleaned_data.get('text')
            }
            receieverName = form.cleaned_data.get('receiverEmail')
           
            form.saveEmail({'email' : receieverName },data)
            messages.success(request , f'Mail sent successfully to {receieverName}')
            return redirect('pmail-login-home')
    else:
        form = UserEmailForm()
    return render(request , 'inbox/compose_email.html',{'form' : form})

