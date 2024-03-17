from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse_lazy, reverse

from cns import settings
from service.models import Provider
from user.forms import ForgotPasswordForm
from user.models import User, UserSignup, Login_main

from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'base.html')


def choose_register(request):
    return render(request, 'register/choose_signup.html')


def provide_signup(request):
    return render(request, 'register/provider-signup.html')


def user_signup(request):
    return render(request, 'register/user-signup.html')

def user_signin(request):
    return render(request, 'login/login.html')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            return redirect('user:reset_password')  # Redirect to password reset page or any other page
    else:
        form = ForgotPasswordForm()

    return render(request, 'login/forgot_password.html', {'form': form})


def reset_password(request):
    return render(request, 'login/reset_password.html')

def provider_dashboard(request):
    return render(request, 'provider/provider-dashboard.html')
