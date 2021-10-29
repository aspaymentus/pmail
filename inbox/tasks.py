from celery import shared_task
from databaselayer.connection import dbConnection
from databaselayer import queries
from time import sleep
from django_celery_results.models import TaskResult
@shared_task
def sendEmail(findFilter,data):
    sleep(2)
    queries.saveEmailQuery(findFilter,data)
    delete_from_outbox(data)

def insert_into_outbox(data):
    user_email = data['senderEmail']
    del data['senderEmail']
    queries.put_message_in_outbox({'email' : user_email}, data)

def delete_from_outbox(data):
    queries.delete_message_from_outbox({'username' : data['senderName']}, data["message_id"])
