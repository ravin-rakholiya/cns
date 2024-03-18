from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse_lazy, reverse
from pyexpat.errors import messages

from cns import settings
from service.models import Provider
from user.forms import *
from user.models import User, UserSignup, Login_main

from django.http import HttpResponseRedirect


def index(request):
    context = {"base_template":"base.html"}
    return render(request, 'base.html', context=context)


def choose_register(request):
    context = {"base_template":"base.html"}
    return render(request, 'register/choose_signup.html', context=context)

def provider_signup(request):
    context = {"base_template": "base.html"}
    if request.method == 'POST':
        form = ProviderSignupForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            names = form.cleaned_data['name']
            emails = form.cleaned_data['email']
            phones = form.cleaned_data['phone']
            passwords = form.cleaned_data['password']

            # Save the data to the database
            provider = Provider(name=names, email=emails, phone=phones, password=passwords)
            provider.save()

            # Redirect to a success page or return a success message
            return redirect('user:index')  # Redirect to the index page
    else:
        form = ProviderSignupForm()
    context['form'] = form
    return render(request, 'register/provider-signup.html', context=context)


def user_signup(request):
    context = {"base_template":"base.html"}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Create a new User_s object and save it to the database

        user = UserSignup(name=name, email=email, phone=phone, password=password)
        user.save()

        # Redirect the user to a different page after signup
        return redirect('user:index')
    else:
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
    context = {"base_template":"provider-base.html", 'active_menu': 'services', 'user_type':"customer", "active_header":"providers"}
    return render(request, 'provider/provider-services.html', context=context)

def provider_booking(request):
    context = {"base_template":"provider-base.html", 'active_menu': 'bookings', "active_header":"providers"}
    return render(request, 'provider/provider-booking.html', context=context)


def customer_booking(request):
    context = {"base_template":"base.html",  "active_menu": "bookings",
        "user_name": "John Smith1",
        "member_since": "Sep 2021",'user_type':"customer", "active_header":"customers"}
    return render(request, 'customer/customer-booking.html', context=context)





def provider_dashboard(request):
    return render(request, 'provider/provider-dashboard.html')


def customer_profile_creation(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST)
        address_form = AddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save(commit=False)
            address = address_form.save(commit=False)
            user.save()
            address.user = user
            address.save()
            return redirect('success_page')
    else:
        user_form = UserProfileForm()
        address_form = AddressForm()
    return render(request, 'customer/customer_profile_creation.html', {'user_form': user_form, 'address_form': address_form})


def dashboard(request):
    services = [
        {
            "link": "service-details.html",
            "image": "../../static/assets/img/services/service-01.jpg",
            "category": "Plumbing",
            "provider_image": "../../static/assets/img/profiles/avatar-05.jpg",
            "title": "Pipe Installation & Repair",
            "location": "New York, NY, USA",
            "rating": "4.8",
            "price": "$30.00",
            # "old_price": "$45.00"
        },
        {
            "link": "service-details.html",
            "image": "../../static/assets/img/services/service-02.jpg",
            "category": "Electrical",
            "provider_image": "../../static/assets/img/profiles/avatar-06.jpg",
            "title": "Electrical Installation",
            "location": "Los Angeles, CA, USA",
            "rating": "4.9",
            "price": "$50.00",
            "old_price": "$60.00"
        },
        {
            "link": "service-details.html",
            "image": "../../static/assets/img/services/service-03.jpg",
            "category": "Painting",
            "provider_image": "../../static/assets/img/profiles/avatar-07.jpg",
            "title": "House Painting",
            "location": "Chicago, IL, USA",
            "rating": "4.7",
            "price": "$40.00",
            # "old_price": "$55.00"
        },
    ]
    return render(request, 'index.html', {'services': services})
