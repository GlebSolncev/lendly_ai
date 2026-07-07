import binascii
import os
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as log_in, logout as log_out, authenticate

from base.mail_service import mail_service
from user.models import User


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()


def login(request):
    if request.user.is_authenticated:
        return redirect('account')


    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            password = request.POST.get('password')

            # Authenticating the user
            user = authenticate(username=user.username, password=password)

            if user:
                log_in(request, user)
                return redirect('account')
            else:
                # Displaying an error message if authentication fails
                messages.error(request, 'Invalid email or password. Please try again.')

        except User.DoesNotExist:
            # Displaying an error message if the user does not exist
            messages.error(request, 'User with this email does not exist. Please sign up.')

            

    return render(request, 'login.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        # Check if a user with this email already exists
        if User.objects.filter(email=request.POST.get('email')).exists():
            # Display an error message if the user already exists
            messages.error(request, 'User with this email already exists. Please log in.')
            return redirect('sign_up') # Redirect back to the signup page

        user = User()
        user.username = request.POST.get('email')
        user.email = request.POST.get('email')
        user.source = request.POST.get('source')

        if password == repeat_password:
            user.set_password(request.POST.get('password'))
            user.save()
            log_in(request, user)
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('sign_up') # Redirect back to the signup page
        
        
        return redirect('account')

    return render(request, 'sign_up.html')


def logout(request):
    log_out(request)
    return redirect('index')


def reset_password(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if not user:
            return redirect('reset_password')
        else:
            user = user[0]
        user.reset_password_code = generate_key()
        mail_service.send_reset_password_email(user.email, user.reset_password_code)
        user.save()
        return redirect('login')

    return render(request, 'reset_password.html')


def restore_password(request):
    user = User.objects.filter(reset_password_code=request.GET.get('code'))
    if not user and user.reset_password_code != '':
        return redirect('index')
    else:
        user = user[0]

    if request.method == 'POST':
        user.reset_password_code = ''
        user.set_password(request.POST.get('password'))
        user.save()
        log_in(request, user)
        return redirect('account')

    return render(request, 'restore_password.html')
