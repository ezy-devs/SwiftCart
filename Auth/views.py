from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserCreationForm
from Store.views import home
from .forms import PasswordResetForm, ForgetPasswordForm, LoginForm, RegisterForm, UpdateProfileForm
from payment.forms import ShippingForm
from payment.models import ShippingInfo


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'username already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user = authenticate(request, username=username, password=password)
                
                login(request, user)
                messages.success(request, 'Login successfully!')
                return redirect(home)
        else:
            messages.error(request, 'Password does not match')
            return redirect(register)

    return render(request, 'auth/register.html')

    
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
         
        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                
                messages.success(request, 'Login successfully!')
                return redirect('home')
        else:
            messages.error(request, 'Records for not found')
            return redirect('login')
    else:
        
        return render(request, 'auth/login.html')


def logout_user(request):
    messages.success(request, 'User logged out!')
    logout(request)
    return redirect('home')


@login_required(login_url='login/')
def password_reset(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = PasswordResetForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password reset successfully!')
            login(request, user)
            return redirect('profile', user)
        else: 
            messages.error(request, 'Password does not Match')
            for error in list(form.errors.values()):

                messages.error(request, error)
                return redirect('password-reset', user)
    else:

        form = PasswordResetForm(user)
        
        return render(request, 'auth/password_reset.html', {'form': form})

def error_404(request):
     return render(request, 'auth/404.html', {})

def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', request.user)
        else:
            messages.success(request, 'Request could not be completed, try again!')
            return redirect('profile', request.user)

# @login_required(login_url='login/')
def profile(request, username):
    if request.user.is_authenticated:

        username = request.user
        try:
            get_object_or_404(User, username=username)

         
        except User.objects.get(username=username).DoesNotExist:
            messages.success(request, 'User not found, please Login')
            return redirect('login')
        
        form = UpdateProfileForm(instance=request.user.profile)
        try:

            user_shipping_info = ShippingInfo.objects.filter(user=request.user).first()
            shipping_Form = ShippingForm(instance=user_shipping_info)

        except ShippingInfo.objects.filter(user=request.user).DoesNotExist:
            shipping_Form = ShippingForm()
            
        return render(request, 'auth/profile.html', {'username': username, 'form':form, 'shipping_Form':shipping_Form})
    else:
        messages.error(request, 'You have to login to access that page')
        return redirect(error_404)


