from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Please fill all fields')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('home')
            else:
                messages.error(request, 'Invalid user or password')
    return render(request, 'accounts/login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, 'Please fill all fields')
        else:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                message = render_to_string('accounts/forgot_password.html', {
                    'user': user,
                    'uid': uid,
                    'token': token
                })
                send_mail('reset Password', message, ' [email protected]', [email])
                messages.success(request, 'Password reset email sent')
            else:
                messages.error(request, 'Email does not exist')
    return render(request, 'accounts/forgot_password.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pwd1 = request.POST['password1']
        pwd2 = request.POST['password2']
        
        if pwd1 == pwd2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=pwd1)
                user.save()
                messages.success(request, 'Account successfully created')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
    else:
        form = ProfileForm()
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            form = ProfileForm(instance=profile)
        else:
            form = ProfileForm()
    return render(request, 'accounts/create_profile.html', {'form': form})

@login_required
def view_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    return render(request, 'accounts/view_profile.html', {'profile': profile})   



  
