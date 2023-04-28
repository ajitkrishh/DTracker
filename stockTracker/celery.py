from __future__ import absolute_import,unicode_literals
import os

from celery import Celery
from django.conf import settings
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'stockTracker.settings')
app = Celery('stockTracker')
app.conf.enable_utc = False
app.conf.update(timezone = "Asia/Kolkata")

app.config_from_object('django.conf:settings' , namespace = "CELERY")
app.conf.beat_schedule = {
    'every-1-minute' : {
        'task' : 'mainapp.tasks.clean_stock_track',
        'schedule': 60,
        'args' : ()
    }
}


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'requests :  {self.request!r}')