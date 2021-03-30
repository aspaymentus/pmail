from django.core.exceptions import ValidationError
from django.utils.translation import ugettext,ugettext_lazy as _
from databaselayer.connection import dbConnection
from databaselayer import queries

def validatorUsername(username):
    myCollection = dbConnection('Pmail' , 'user_data')
    if queries.findQuery(myCollection,{'username' : username}):
        raise ValidationError(_('%(username)s Already Exists!'),
                                params={'username' : username}
                                )

def validatorEmail(email):
    myCollection = dbConnection('Pmail' , 'user_data')
    if queries.findQuery(myCollection,{'email' : email}):
        raise ValidationError(_('An account with this email Already Exists!'),
                                 )