from django.shortcuts import render
from .forms import *
from .models import *

# Create your views here.
def dashboard(request):
    # You might fetch some data here...
    return render(request, 'monitoring/dashboard.html')

def notification(request):
    # You might fetch some data here...
    return render(request, 'monitoring/notification.html')

def website(request):
   form = WebsiteForm()
   if request.method == 'POST':
          form = WebsiteForm(request.POST)
          if form.is_valid():
            model = form.save(commit=False)
            model.user = request.user
   context = {'form': form}
   return render(request, 'monitoring/website.html', context)

def feedback(request):
    form = FeedbackForm() 
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
             model = form.save(commit=False)
             model.user = request.user
    context = {'form': form}
    return render(request, 'monitoring/feedback.html', context)

def Issue(request):
    form = IssueForm()
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.user = request.user
    context = {'form': form}
    return render(request, 'monitoring/Issue.html', context)