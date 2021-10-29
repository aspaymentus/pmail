from django.shortcuts import render,redirect
from .forms import UserRegisterForm,UserLoginForm
from databaselayer.connection import dbConnection
from databaselayer import queries
from django.contrib import messages
from django.utils import timezone


# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = {
                "username" : form.cleaned_data.get('username'),
                "email" : form.cleaned_data.get('email'),
                "password" : form.cleaned_data.get('password'),
                "date_joined" : timezone.now(),
                "is_login" : False
                
            }
            form.saveData(data)
            username = form.cleaned_data.get('username')
            myCollection = dbConnection('Pmail' , 'inbox')
            queries.createCollectionQuery(myCollection,{'username' : username , 'email' : form.cleaned_data.get('email'),"messages" : []})
            myCollection = dbConnection('Pmail' , 'outbox')
            queries.createCollectionQuery(myCollection,{'username' : username , 'email' : form.cleaned_data.get('email'),"messages" : []})
            messages.success(request,f'Account created for {username}!')
            return redirect('pmail-home')
    else:   
        form = UserRegisterForm()
    return render(request , 'users/create_user.html',{'form' : form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            myCollection = dbConnection('Pmail' , 'user_data')
            data = queries.findWithProjectionQuery(myCollection , {'username' : username} , {'username' : 1 , 'password' : 1})
            try:
                username == data['username'] and password == data['password']
                queries.loginQuery(username,status=True)
                messages.success(request , f'Successfully Logged In as {username}')
                return redirect('pmail-login-home')
            except:
                messages.warning(request,f'Invalid username or Password')
                return redirect('user-login')
    else:
        form = UserLoginForm()
    return render(request , 'users/login.html' , {'form' : form})

def logout(request):
    myCollection = dbConnection('Pmail' , 'user_data')
    queries.logoutQuery(status = False)
    messages.success(request , f'Successfully Logged Out')
    return redirect('pmail-home')
