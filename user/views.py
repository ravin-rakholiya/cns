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
    context = {"base_template":"base.html"}
    return render(request, 'base.html', context=context)


def choose_register(request):
    context = {"base_template":"base.html"}
    return render(request, 'register/choose_signup.html', context=context)


def provide_signup(request):
    context = {"base_template":"base.html"}
    return render(request, 'register/provider-signup.html', context=context)


def user_signup(request):
    context = {"base_template":"base.html"}
    return render(request, 'register/user-signup.html', context=context)

def user_signin(request):
    context = {"base_template":"base.html"}
    return render(request, 'login/login.html', context=context)

def forgot_password(request):
    context = {"base_template":"base.html"}
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            return redirect('user:reset_password', context=context)  # Redirect to password reset page or any other page
    else:
        form = ForgotPasswordForm()
    context['form']=form
    return render(request, 'login/forgot_password.html', context=context)


def reset_password(request):
    context = {"base_template":"base.html"}
    return render(request, 'login/reset_password.html', context=context)

def provider_services(request):
    context = {"base_template":"provider-base.html", 'active_menu': 'services', 'user_type':"customer"}
    return render(request, 'provider/provider-services.html', context=context)

def provider_booking(request):
    context = {"base_template":"provider-base.html", 'active_menu': 'bookings'}
    return render(request, 'provider/provider-booking.html', context=context)


def customer_booking(request):
    context = {"base_template":"base.html",  "active_menu": "bookings",
        "user_name": "John Smith1",
        "member_since": "Sep 2021",'user_type':"customer"}
    return render(request, 'customer/customer-booking.html', context=context)




