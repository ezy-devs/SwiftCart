from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from Store.views import home
from .forms import PasswordReset

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already used')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'username already used')
            return redirect('register')
        else:
            user = User.objects.create(username=username, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfully!')
                return redirect(home)

    return render(request, 'auth/register.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Wrong email or password')
            return redirect('login')

    return render(request, 'auth/login.html')

def logout_user(request):
    logout(request)
    return redirect(home)

@login_required(login_url='login/')
def password_reset(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password reset successfully!')
            return redirect('profile', user)
        else: 
            messages.error(request, 'Password does not Match')
            form.error_messages(request)
            return redirect('password-reset', user)

    form = SetPasswordForm(user)
    
    return render(request, 'auth/password_reset.html', {'form': form})

@login_required(login_url='login/')
def profile(request, username):
    username = request.user
    try:
        get_object_or_404(User, username=username)
        return render(request, 'auth/profile.html', {'username': username})
    
    except User.objects.get(username=username).DoesNotExist:
        messages.success(request, 'User not found, please Login')
        return redirect('register')
    


    