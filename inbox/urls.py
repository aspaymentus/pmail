from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name = 'pmail-home'),
    path('home/',views.loginRedirect,name = 'pmail-login-home'),
    path("inbox/" , views.inbox ,name = "mail-inbox"),
    path("compose/",views.compose, name = "mail-compose"),
    path("outbox/",views.outbox,name = 'mail-outbox'),
    path("checkSent/",views.check_mail_status,name = 'mail-status')
]