from .models import Website, Measurement, Notification, Issue
from .execution import check_website_status, ping_website
from celery import shared_task
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def check_status(*args):
    print('Task started', args)
    url = args[0]
    username = args[1]
    website_id = args[2]
    user = User.objects.get(username=username)
    website = Website.objects.get(id=website_id)
    results = ping_website(url)
    print(results) #results = {    'url': url,'latency': None,'status_code': None,'error': None,'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'}
    m = Measurement(website=website, 
                    latency=results['latency'] or -1,
                    status_code=results['status_code'],
                    error=results['error'])
    
    m.save()
    if results['status_code'] != 200:
        n = Notification(website=website, message=f'Website is down with status code {results[2]}')
        n.save()
        send_mail(
            'Website Down',
            f'Your website {url} is down with status code {results[2]}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
    print('Task completed')
    return 'Task completed'

from celery import shared_task 
from time import sleep

@shared_task
def my_task():
    for i in range(11):
        print(i)
        sleep(1)
    return "Task Complete!"


if __name__ == '__main__':
    check_status(('https://www.digipodium.com', 'zaidkamil', 1))
