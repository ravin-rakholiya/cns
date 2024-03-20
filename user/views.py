from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse_lazy, reverse
from pyexpat.errors import messages
from cns import settings
from service.models import *
from user.forms import *
from user.models import *
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from user.templatetags.custom_message import custom_message
from user.scripts import *
from notifications.scripts import *


def index(request):
    context = {"base_template":"base.html"}
    return render(request, 'base.html', context=context)


class ChooseRegisterView(View):
    template_name = 'register/choose_signup.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        context = {'base_template': self.base_template}
        return render(request, self.template_name, context=context)


class ProviderSignupView(View):
    template_name = 'register/provider-signup.html'
    base_template = 'base.html'
    form_class = ProviderSignupForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'base_template': self.base_template, 'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'base_template': self.base_template, 'form': form}
        if form.is_valid():
            # Process the data in form.cleaned_data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = User.objects.filter(email = email)
            if user:
                if not user.last().email_verified:
                    messages.error(request, "Please verify your email.")
                    return redirect(reverse('user:verify_email'))
            user_type = UserType.objects.get(user_type = 'provider')
            user = User.objects.create(email = email, user_type = user_type, first_name = first_name, last_name = last_name, phone_number=phone)
            user.set_password(password)
            user.email_verified = False
            user.save()
            verification_token = generate_verification_token()
            verification_link = generate_user_account_verification_link(verification_token, "user/verify-mail?token=")
            EmailVerification.objects.get_or_create(email_to = user, verification_token = verification_token)
            send_account_verification_mail("Verify your email to create your USH Account",first_name, verification_link, email)
            # Redirect to a success page or return a success message
            context['success_message'] = "Signup successful!"
            return redirect('user:verify_email')  # Redirect to the index page

        
        return render(request, self.template_name, context=context)

class VerifyEmailView(View):
    template_name = 'register/verify_email.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        context = {"base_template": self.base_template}
        return render(request, self.template_name, context=context)


class VerifyEmailSuccessView(View):
    template_name = 'login/login.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        context = {"base_template": self.base_template}
        verification_token = request.GET.get('token', None)

        if not verification_token:
            context['verification_token'] = False
            return render(request, self.template_name, context=context)

        email_verification = get_object_or_404(EmailVerification, verification_token=verification_token)
        user = email_verification.email_to
        if user and email_verification.validate_email(user, verification_token):
            if not user.email_verified:
                user.email_verified = True
                user.save()
                context['verification_token'] = True
        else:
            context['verification_token'] = False

        return render(request, self.template_name, context=context)

class UserSignupView(View):
    template_name = 'register/user_signup.html'
    base_template = "base.html"
    form_class = UserSignupForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"base_template": self.base_template, "form": form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'base_template': self.base_template, 'form': form}
        if form.is_valid():
            # Process form data and redirect after successful form submission
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = User.objects.filter(email = email)
            if user:
                if not user.last().email_verified:
                    messages.error(request, "Please verify your email.")
                    return redirect(reverse('user:verify_email'))
            user = User.objects.create(email = email, first_name = first_name, last_name = last_name, phone_number=phone)
            user.set_password(password)
            user.email_verified = False
            user.save()
            verification_token = generate_verification_token()
            verification_link = generate_user_account_verification_link(verification_token, "user/verify-mail?token=")
            EmailVerification.objects.get_or_create(email_to = user, verification_token = verification_token)
            send_account_verification_mail("Verify your email to create your USH Account",first_name, verification_link, email)
            # Redirect to a success page or return a success message
            context['success_message'] = "Signup successful!"
            # Perform actions with form data (e.g., save to database)
            return redirect('user:verify_email')  # Change this to your desired success URL
        else:
            context = {"base_template": "base.html", "form": form}
            return render(request, self.template_name, context=context)


class UserSigninView(View):
    template_name = 'login/login.html'
    base_template = "base.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        context = {"base_template": self.base_template, "form": self.form_class}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'base_template': self.base_template, 'form': form}
        if form.is_valid():
            # Process form data and redirect after successful form submission
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            email = email.lower()
            user = User.objects.filter(email=email).first()
            if user:
                if user.email_verified == False:
                    context = {"base_template": "base.html", "form": form, "alert":"Please Verify Your Email"}
                    return render(request, self.template_name, context=context)
            else:
                context = {"base_template": "base.html", "form": form, "alert":"Email Does Not Exist, Please Make Sign up."}
                return render(request, self.template_name, context=context)
            if user.check_password(password):
                token = user.get_tokens_for_user()
                print("179----", token)
                context['success_message'] = "SignIn successful!"
                return redirect('info_pages:about_us')
            else:
                context = {"base_template": "base.html", "form": form, "alert":"User does not exist with this credentials."}
                return render(request, self.template_name, context=context)
        else:
            context = {"base_template": "base.html", "form": form}
            return render(request, self.template_name, context=context)


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


def provider_list(request):
    context = {"base_template":"provider-base.html", 'active_menu': 'bookings', "active_header":"providers"}
    return render(request, 'provider/provider-list.html', context=context)

def provider_details(request):
    context = {"base_template":"provider-base.html", "active_header":"providers"}
    return render(request, 'provider/provider-details.html', context=context)


def customer_booking(request):
    context = {"base_template":"base.html",  "active_menu": "bookings",
        "user_name": "John Smith1",
        "member_since": "Sep 2021",'user_type':"customer", "active_header":"customers"}
    return render(request, 'customer/customer-booking.html', context=context)


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
