from django.shortcuts import render

# Create your views here.
def dashboard(request):
    # You might fetch some data here...
    return render(request, 'dashboard.html')

def notification(request):
    # You might fetch some data here...
    return render(request, 'notification.html')

def website(request):
    # You might fetch some data here...
    return render(request, 'website.html')