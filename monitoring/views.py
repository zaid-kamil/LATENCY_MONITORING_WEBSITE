from django.shortcuts import render
from .forms import *
from .models import *

# Create your views here.
def dashboard(request):

    if request.method == 'POST':
        form = LatencyForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # (For example, you could update a model or send an email)
            pass
    else:
        form = LatencyForm()

    return render(request, 'monitoring/dashboard.html',{'form': form})
   

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

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')
