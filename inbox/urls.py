from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name = 'pmail-home'),
    path('home/',views.loginRedirect,name = 'pmail-login-home'),
    path("inbox/" , views.inbox ,name = "mail-inbox"),
    path("compose/",views.compose, name = "mail-compose")
]