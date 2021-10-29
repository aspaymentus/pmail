from django.shortcuts import render,redirect
from django.http import HttpResponse
from pymongo import message
from .forms import UserEmailForm
from django.contrib import messages
from databaselayer import queries, connection
import random
from .tasks import sendEmail,insert_into_outbox
from django_celery_results.models import TaskResult
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
            
            inbox_data = {
                "senderName" : activeUser['username'],
                "senderEmail" : activeUser['email'],
                "subject" : form.cleaned_data.get('subject'),
                "message" : form.cleaned_data.get('text'),
                "message_id" : random.randint(1,1000000000)
            }
            receieverName = form.cleaned_data.get('receiverEmail')
            outbox_data = {
                "senderEmail" : inbox_data['senderEmail'],
                "receiverName" : receieverName,
                "subject" : inbox_data['subject'],
                "message" : inbox_data['message'],
                "message_id" : inbox_data['message_id']
            }
            insert_into_outbox(outbox_data)
            sendEmail.delay({'email' : receieverName },inbox_data)
            messages.success(request , f'Mail will be sent shortly to {receieverName}')
            return redirect('pmail-login-home')
    else:
        form = UserEmailForm()
    return render(request , 'inbox/compose_email.html',{'form' : form})

def outbox(request):
    myCollection = connection.dbConnection('Pmail' , 'user_data')
    email = queries.findWithProjectionQuery(myCollection,{'is_login' : True} , {'email' : 1})['email']
    myCollection = connection.dbConnection('Pmail' , 'outbox')
    data = queries.findWithProjectionQuery(myCollection , {'email' : email} , {'messages' : 1})
    return render(request , 'inbox/outbox_view.html',context = {'mails' : data['messages']})

def check_mail_status(request):
    if request.is_ajax():
        status = TaskResult.objects.values("status")
        if status[0]["status"] == "SUCCESS":
            return HttpResponse("Done")
    return HttpResponse("Not Done")
