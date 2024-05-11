import os

from celery import Celery
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
        'check-status-every-30-seconds': {
        'task': 'check_status',
        'schedule': 30.0,
    },
    'check-status-every-day_at_10': {
        'task': 'check_status',
        'schedule': crontab(hour=10, minute=0),
    },
    
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    return 'Task completed'



# Path: config/__init__.py

# activate redis 
# sudo service redis-server start

# run celery command
# celery -A config beat -l info


    
