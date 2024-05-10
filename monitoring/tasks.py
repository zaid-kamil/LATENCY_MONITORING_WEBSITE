from .models import Website, Measurement, Notification, Issue
from celery import shared_task
from .execution import check_website_status, ping_website
from datetime import datetime
from django.contrib.auth.models import User

# run celery beat
from celery.schedules import crontab
from celery import Celery

app = Celery('config', broker='redis://localhost:6379/0')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, check_status.s(), name='add every 10')



@shared_task
def check_status():
    websites = Website.objects.all()
    for website in websites:
        results = ping_website(website.url)
        Measurement.objects.create(
            website=website,
            timestamp=datetime.now(),
            latency=results['ping_time'],
            status_code=results['status_code'],
            error=results['error']
        )
        if results['status_code'] != 200:
            Notification.objects.create(
                website=website,
                timestamp=datetime.now(),
                message=f'The website {website.url} is down'
            )
            for user in User.objects.all():
                Issue.objects.create(
                    website=website,
                    timestamp=datetime.now(),
                    message=f'The website {website.url} is down',
                    user=user
                )
    return 'Task completed'

