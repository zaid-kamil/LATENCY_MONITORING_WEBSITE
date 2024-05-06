from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
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
        user = User.objects.filter(email=email).first()
        token = default_token_generator.make_token(user)
        mail_subject = 'Reset your password'
        message = render_to_string('accounts/reset_password.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token
        })  
        send_mail(mail_subject, message, 'admin@mywebsiite.com', [email])
        return redirect('password_reset_done')
    return render(request, 'accounts/forgot_password.html')

def reset_password(request, otp):
    try:
        uid = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password = request.POST.get('password')
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('login')
            return render(request, 'accounts/forgot_password.html')
        else:
           messages.error(request, 'Password reset unsuccessful. The link is invalid.')
        return redirect('login')    


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
    return render(request, 'create_profile.html', {'form': form})



  
