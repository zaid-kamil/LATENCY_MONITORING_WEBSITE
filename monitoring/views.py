from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.
def dashboard(request):
    websites = Website.objects.filter(user=request.user)

    return render(request, 'monitoring/dashboard.html', {'websites': websites})
   

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
            model.save()
            messages.success(request, 'Website added successfully')
            return redirect('dashboard')
   context = {'form': form}
   return render(request, 'monitoring/website.html', context)

def view_website(request, pk):  
    website = Website.objects.get(id=pk)
    context = {'website': website}
    return render(request, 'monitoring/view_website.html', context)

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

def delete_website(request, pk):
    website = Website.objects.get(id=pk)
    website.delete()
    messages.success(request, 'Website deleted successfully')
    return redirect('dashboard')

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
