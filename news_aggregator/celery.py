from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator.settings')

app = Celery('news_aggregator')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

from celery.schedules import crontab
from datetime import timedelta

app.conf.beat_schedule = {
    'execute-my-task-every-day': {
        'task': 'news_parser.tasks.my_scheduled_task',
        # 'schedule': crontab(hour=0, minute=0),  # Executes daily at midnight
        # 'schedule': timedelta(seconds=10),  # Executes every 10 seconds
        'schedule' : crontab(minute='*/5'),
    },
}
