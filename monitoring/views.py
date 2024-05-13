from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .tasks import *

# Create your views here.
def dashboard(request):
    websites = Website.objects.filter(user=request.user)
    website_count = Website.objects.filter(user=request.user).count()
    return render(request, 'monitoring/dashboard.html', {'websites': websites, 'website_count': website_count})
 
def notification(request):
   return render(request, 'monitoring/notification.html')

@login_required
def website(request):
   form = WebsiteForm()
   if request.method == 'POST':
          form = WebsiteForm(request.POST)
          if form.is_valid():
            model = form.save(commit=False)
            model.user = request.user
            model.save()
            messages.success(request, 'Website added successfully')
            return redirect('dashboard')
   context = {'form': form}
   return render(request, 'monitoring/website.html', context)

# import paginator
from django.core.paginator import Paginator
import json
@login_required
def view_website(request, pk):  
    website = Website.objects.get(id=pk)
    measurements = Measurement.objects.filter(website=website).order_by('-timestamp')
    for m in measurements:
        m.status = 'Up' if m.status_code == 200 else 'Down'
        m.latency = m.latency * 1000 or -1
    paginator = Paginator(measurements, 10)
    page_number = request.GET.get('page')
    measurements = paginator.get_page(page_number)
    date_list = Measurement.objects.filter(website=website).values_list('timestamp', flat=True)[:50]
    time_list = []
    clean_date_list = []
    for date in date_list:
        cdate = date.strftime('%Y-%m-%d')
        time = date.strftime('%H:%M:%S')
        time_list.append(time)
        clean_date_list.append(cdate)
    latency_list = Measurement.objects.filter(website=website).values_list('latency', flat=True).order_by('-timestamp')[:50]
    status_code_list = Measurement.objects.filter(website=website).values_list('status_code', flat=True).order_by('-timestamp')[:50]
    # convert latency in milliseconds
    latency_list = [latency * 1000 for latency in latency_list]
    # convert status code into list
    status_code_list = list(status_code_list)
    # convert latency into list
    latency_list = list(latency_list)
    context = {
        'website': website, 
        'm': measurements,
        'time_list': json.dumps(time_list), 
        'date_list': json.dumps(clean_date_list),
        'latency_list': json.dumps(latency_list),
        'status_code_list': json.dumps(status_code_list)
        }
    return render(request, 'monitoring/view_website.html', context)

@login_required
def edit_website(request, pk):
    website = Website.objects.get(id=pk)
    form = WebsiteForm(instance=website)
    if request.method == 'POST':
        form = WebsiteForm(request.POST, instance=website)
        if form.is_valid():
            form.save()
            messages.success(request, 'Website updated successfully')
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'monitoring/website.html', context)

@login_required
def delete_website(request, pk):
    website = Website.objects.get(id=pk)
    website.delete()
    # remove the task from the scheduler
    try:
        schedule_name = f'{request.user.username}_{website.url.replace(".", "_")}'
        print(schedule_name)
        task = PeriodicTask.objects.get(name=schedule_name)
        task.delete()
    except PeriodicTask.DoesNotExist:
        print('Task does not exist', schedule_name)

    messages.success(request, 'Website deleted successfully')
    return redirect('dashboard')

def create_new_feedback(request):
    form = FeedbackForm() 
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
             model = form.save(commit=False)
             model.user = request.user
             model.save()
        messages.success(request, 'Feedback added successfully')
    context = {'form': form}
    
    return render(request, 'monitoring/feedback.html', context)

def view_feedback(request):
    feedback_list = Feedback.objects.all()
    return render(request, 'monitoring/view_feedback.html', {'feedback_list': feedback_list})

@login_required
def create_new_issue(request):
    form = IssueForm()
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user = request.user
            model.save()
            messages.success(request, 'Issue added successfully')
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'monitoring/Issue.html', context)

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and email and subject and message:
            c = contact(name=name, email=email, subject=subject, message=message)
            c.save()
            messages.success(request, 'Message sent successfully')
        else:
            messages.error(request, 'Please fill all the fields')
    return render(request, 'contact.html')

def subscriber_view(request):
   if request.method == 'POST':
        email = request.POST.get('email')
        try:
            Subscriber.objects.get(email=email)
            messages.error(request, 'Email already exists')
        except Subscriber.DoesNotExist:
            s = Subscriber(email=email)
            s.save()
            messages.success(request, 'Subscribed successfully')
   return render(request, 'index.html')

# run task when the view is called
def run_task(request):
    my_task.delay()
    messages.success(request, 'Task started successfully')
    return redirect('dashboard')
        
from accounts.models import Profile
import json

def schedule_website_monitor(request):
    websites = Website.objects.all()
    

    for website in websites:
        interval,_ = IntervalSchedule.objects.get_or_create(
            every = website.check_frequency,
            period = IntervalSchedule.SECONDS #  switch to minutes
        )
        try:
            PeriodicTask.objects.create(
            interval = interval,
            name = f'{request.user.username}_{website.url.replace(".", "_")}',
            task = check_status,
            args = json.dumps([website.url, request.user.username, website.id]))
            messages.success(request, f'Motnitoring Task scheduled successfully for {website.url}')
        except Exception as e:
            raise e
            messages.error(request, f'Task already exists for {website.url}')
    return redirect('dashboard')
