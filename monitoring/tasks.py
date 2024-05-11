from .models import Website, Measurement, Notification, Issue
from celery import shared_task
from .execution import check_website_status, ping_website
from datetime import datetime
from django.contrib.auth.models import User
from config.celery import app

@shared_task(bind=True, name='check_status')
def check_status(*args):
    print('Task started', args)
    websites = Website.objects.all()
    for website in websites:
        print(f'Checking status of {website.url}')
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


@app.task(bind=True, name='print_hello')
def print_hello():
    print('Hello world')
