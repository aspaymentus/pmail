import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pmail.settings')

app = Celery('pmail')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
# celery beat settings
app.conf.beat_schedule = {
    "send_mail_every_year_1" : {
        "task" : "inbox.tasks.sendEmail",
        "schedule" : crontab(minute=11 , hour=15),
        "args" : ({"abc"  : "abc"},{"xyz" : "xyz"})
    }
}
app.conf.timezone = "ASIA/KOLKATA"
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')