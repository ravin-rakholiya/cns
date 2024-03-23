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
from user.utils import *
from django.views.generic import TemplateView
from service.models import *


class DashboardView(View):
    template_name = 'index.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        action = request.GET.get('action', None)
        if action=='logout':
            request.session.pop('access_token', None)
        context = {}
        try:
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
            context['services'] = services
            context['base_template'] = 'base.html'
            context['active_header'] = 'home'
            try:
                user = User.objects.get(pk=request.user_id)
                context['user_type'] = user.user_type.user_type
                context['user'] = user
            except Exception as e:
                pass
            return render(request, self.template_name, context=context)
        except Exception as e:
            context = {'base_template': self.base_template}
            return render(request, self.template_name, context=context)

class ChooseRegisterView(View):
    template_name = 'register/choose_signup.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            if user.user_type.user_type=="provider":
                return redirect('user:provider_booking')
            return redirect('user:customer_booking')
        except Exception as e:
            context = {'base_template': self.base_template}
            return render(request, self.template_name, context=context)


class ProviderSignupView(View):
    template_name = 'register/provider-signup.html'
    base_template = 'base.html'
    form_class = ProviderSignupForm

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            if user.user_type.user_type=="provider":
                return redirect('user:provider_booking')
            return redirect('user:customer_booking')
        except Exception as e:
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
            context['user'] = user
            return redirect('user:verify_email')  # Redirect to the index page

        
        return render(request, self.template_name, context=context)

class VerifyEmailView(View):
    template_name = 'register/verify_email.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            if user.user_type.user_type=="provider":
                return redirect('user:provider_booking')
            return redirect('user:customer_booking')
        except Exception as e:
            context = {"base_template": self.base_template}
            return render(request, self.template_name, context=context)


class VerifyEmailSuccessView(View):
    template_name = 'login/login.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            if user.user_type.user_type=="provider":
                return redirect('user:provider_booking')
            return redirect('user:customer_booking')
        except Exception as e:
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
        try:
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            if user.user_type.user_type=="provider":
                return redirect('user:provider_booking')
            return redirect('user:customer_booking')
        except Exception as e:
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
            context['user'] = user
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
        try:
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            if user.user_type.user_type=="provider":
                return redirect('user:provider_booking')
            return redirect('user:customer_booking')
        except Exception as e:
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
                store_in_session(request, 'refresh_token', token['refresh'])
                store_in_session(request, 'access_token', token['access'])
                context['success_message'] = "SignIn successful!"
                context['user'] = user
                if user.user_type.user_type=="provider":
                    return redirect('user:provider_booking')
                return redirect('user:customer_booking')
            else:
                context = {"base_template": "base.html", "form": form, "alert":"User does not exist with this credentials."}
                context['user'] = user
                return render(request, self.template_name, context=context)
        else:
            context = {"base_template": "base.html", "form": form}
            return render(request, self.template_name, context=context)


class CustomerProfileView(View):
    template_name = 'customer/customer-profile.html'
    form_class = AccountSettingsForm

    def get_initial_data(self):
        user = User.objects.get(pk=self.request.user_id)
        if user.address == None:
            address = Address.objects.create()
            user.address = address
            user.save()
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'gender': user.gender,
            'bio': user.bio if user.bio else '',
            'add1': user.address.add1 if user.address is not None else '',
            'add2': user.address.add2 if user.address is not None else '',
            'country': user.address.country if user.address is not None else '',
            'provision': user.address.provision if user.address is not None else '',
            'city': user.address.city if user.address is not None else '',
            'postal_code': user.address.postal_code if user.address is not None else '',
            'currency_code': user.currency_code,
            # 'profile_picture_upload': user.profile_picture_upload,  # Uncomment if you have this field in your model
        }
        return initial_data

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user_id
            user = User.objects.get(pk=user_id)
            form = self.form_class(initial=self.get_initial_data())
            context = {
                "base_template": "base.html",
                "active_menu": "settings",
                "user_name": "John Smith1",
                "member_since": "Sep 2021",
                "user_type": user.user_type.user_type,
                "active_header": "customers",
                "form": form,
            }
            context['user'] = user
            return render(request, self.template_name, context=context)
        except Exception as e:
            # Redirect to login page if there's an error
            return redirect('user:user_signin')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {
            "base_template": "base.html",
            "active_menu": "settings",
            "user_name": "John Smith1",
            "member_since": "Sep 2021",
            "user_type": user.user_type.user_type,
            "active_header": "customers",
            "form": form,
        }
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            gender = form.cleaned_data["gender"]
            add1 = form.cleaned_data["add1"]
            add2 = form.cleaned_data["add2"]
            country = form.cleaned_data["country"]
            provision = form.cleaned_data["provision"]
            city = form.cleaned_data["city"]
            postal_code = form.cleaned_data["postal_code"]
            currency_code = form.cleaned_data["currency_code"]
            profile_picture_upload = form.cleaned_data["profile_picture_upload"]
            user = User.objects.get(pk=self.request.user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.gender = gender
            user.currency_code = currency_code
            user.save()

            address = user.address
            address.add1 = add1
            address.add2 = add2
            address.country = country
            address.provision = provision
            address.city = city
            address.postal_code = postal_code
            address.save()
            # Process the form data here if needed
            context['message'] = 'Information Updated Successfully.'
            context['user'] = user
            return render(request, self.template_name, context=context)  # Replace 'success_url' with your actual success URL
        return render(request, self.template_name, context=context)


class ProviderProfileView(View):
    template_name = 'customer/customer-profile.html'
    form_class = AccountSettingsForm

    def get_initial_data(self):
        user = User.objects.get(pk=self.request.user_id)
        if user.address == None:
            address = Address.objects.create()
            user.address = address
            user.save()
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'gender': user.gender,
            'bio': user.bio if user.bio else '',
            'add1': user.address.add1 if user.address is not None else '',
            'add2': user.address.add2 if user.address is not None else '',
            'country': user.address.country if user.address is not None else '',
            'provision': user.address.provision if user.address is not None else '',
            'city': user.address.city if user.address is not None else '',
            'postal_code': user.address.postal_code if user.address is not None else '',
            'currency_code': user.currency_code,
            # 'profile_picture_upload': user.profile_picture_upload,  # Uncomment if you have this field in your model
        }
        return initial_data

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            form = self.form_class(initial=self.get_initial_data())
            context = {"base_template":"base.html",  "active_menu": "settings","user_name": "John Smith1","member_since": "Sep 2021",'user_type':user.user_type.user_type, "active_header":"customers", "form":form}
            context['user'] = user
            return render(request, self.template_name, context=context)
        except Exception as e:
            context = {"base_template": "base.html", "form": LoginForm}
            return render(request, 'login/login.html', context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {"base_template":"base.html",  "active_menu": "settings","user_name": "John Smith1","member_since": "Sep 2021",'user_type':user.user_type.user_type, "active_header":"customers", "form":form}
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            gender = form.cleaned_data["gender"]
            bio = form.cleaned_data["bio"]
            add1 = form.cleaned_data["add1"]
            add2 = form.cleaned_data["add2"]
            country = form.cleaned_data["country"]
            provision = form.cleaned_data["provision"]
            city = form.cleaned_data["city"]
            postal_code = form.cleaned_data["postal_code"]
            currency_code = form.cleaned_data["currency_code"]
            profile_picture_upload = form.cleaned_data["profile_picture_upload"]
            user = User.objects.get(pk=self.request.user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.gender = gender
            user.bio = bio
            user.currency_code = currency_code
            user.save()
            address = user.address
            address.add1 = add1
            address.add2 = add2
            address.country = country
            address.provision = provision
            address.city = city
            address.postal_code = postal_code
            address.save()
            # Process the form data here if needed
            context['message'] = 'Information Updated Successfully.'
            context['user'] = user
            return render(request, self.template_name, context=context)  # Replace 'success_url' with your actual success URL
        return render(request, self.template_name, context=context)

class ForgotPasswordView(View):
    template_name = 'login/forgot-password.html'
    form_class = ForgotPasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"base_template": "base.html", "form": form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {"base_template": "base.html", "form": form}
        if form.is_valid():
            email = form.cleaned_data['email']
            verification_token = generate_verification_token()
            verification_link = generate_user_account_verification_link(verification_token, "user/reset-password?token=")
            user = User.objects.get(email = email)
            EmailVerification.objects.get_or_create(email_to = user, verification_token = verification_token)
            send_account_verification_mail("Reset your password to login in your USH Account", user.first_name, verification_link, email)
            # Redirect to a success page or return a success message
            context['success_message'] = "Verify your Email to Reset the Passowrd!"
            context["alert"] = "Verify your Email to Reset the Passowrd!"
            return redirect('user:user_signin')  # Adjust the URL name as needed
        return render(request, self.template_name, context=context)


class ResetPasswordView(View):
    template_name = 'login/reset-password.html'
    form_class = ReSetPasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"base_template": "base.html", "form": form}
        verification_token = request.GET.get('token', None)
        alert = request.GET.get('alert', None)
        if not verification_token:
            return redirect('user:user_signin')
        try:
            if alert == "password_does_not_match":
                context['alert'] = "Password Does not Match."
                return render(request, self.template_name, context=context)    
        except Exception as e:
            return redirect('user:user_signin') 
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        verification_token = request.POST.get('token')
        context = {"base_template": "base.html", "form": form}
        if form.is_valid():
            password = form.cleaned_data['password1']
            confirm_password = form.cleaned_data['password2']
            if password!=confirm_password:
                context['alert'] = "Password Does not Match."
                return redirect('http://127.0.0.1:8000/user/reset-password?alert=password_does_not_match&token='+verification_token)
            email_verification = get_object_or_404(EmailVerification, verification_token=verification_token)
            user = email_verification.email_to
            if user and email_verification.validate_email(user, verification_token):
                user.set_password(password)
                user.save()
                return redirect('user:user_signin')
            else:
                return redirect('user:user_signin') 
        return render(request, self.template_name, context=context)

class ProviderServicesView(View):
    template_name = 'provider/provider-services.html'
    base_template = "provider-base.html"

    def get(self, request, *args, **kwargs):
        context = {"base_template": self.base_template, 'active_menu': 'services', "active_header": "providers"}
        try:
            user = get_object_or_404(User, pk=request.user_id)
            context['user_type'] = user.user_type.user_type
            context['user'] = user
        except Exception as e:
            context = {"base_template": 'base.html', "form": LoginForm}
            return render(request, 'login/login.html', context=context)
        return render(request, self.template_name, context=context)

def provider_services(request):
    context = {"base_template":"provider-base.html", 'active_menu': 'services', "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
        context['user'] = user
    except Exception as e:
        pass
    return render(request, 'provider/provider-services.html', context=context)

class ProviderBookingView(View):
    template_name = 'provider/provider-booking.html'

    

    def get(self, request, *args, **kwargs):
        context = {"base_template": "provider-base.html", 'active_menu': 'bookings', "active_header": "providers"}
        try:
            user = get_object_or_404(User, pk=request.user_id)
            context['user_type'] = user.user_type.user_type
            context['user'] = user
            provider_bookings = ServiceBooking.objects.filter(service__provider=user).order_by('appointment_time')
            context['provider_bookings'] = provider_bookings

            service_ratings = {}
            for booking in provider_bookings:
                ratings = ServiceRating.objects.filter(service=booking)
                if ratings:
                    service_ratings[booking.id] = generate_string(ratings.last().rate)
            context['service_ratings'] = service_ratings
            # # Instantiate the ReviewForm and include it in the context
            # review_form = RatingForm()
            # context['review_form'] = review_form
        except Exception as e:
            context = {"base_template": 'base.html', "form": LoginForm}
            return HttpResponseRedirect(reverse('user:user_signin'))
        return render(request, self.template_name, context=context)

    # def post(self, request, *args, **kwargs):
    #     form = RatingForm(request.POST)
    #     if form.is_valid():


    #         user_id = request.user_id
    #         user = User.objects.get(pk=user_id)
    #         provider_booking_id = request.POST.get('provider_booking_id')
    #         service_booking = ServiceBooking.objects.get(pk=provider_booking_id)
    #         rating = form.cleaned_data['rating']
    #         comment = form.cleaned_data['comment']
    #         rating = ServiceRating.objects.create(user=user, service = service_booking, rate=float(rating), comment=comment)

    #         # Redirect to a success URL after form submission
    #         return HttpResponseRedirect(reverse('user:provider_booking'))  # Replace 'success_url' with your actual success URL

    #     # If form is not valid, render the form again with validation errors
    #     context = {"base_template": "provider-base.html", 'active_menu': 'bookings', "active_header": "providers"}
    #     context['review_form'] = form  # Pass the form instance with validation errors to the template
    #     return render(request, self.template_name, context=context)

def provider_booking(request):
    context = {"base_template":"provider-base.html", 'active_menu': 'bookings', "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
        context['user'] = user
    except Exception as e:
        context = {"base_template": 'base.html', "form": LoginForm}
        return render(request, 'login/login.html', context=context)
    return render(request, 'provider/provider-booking.html', context=context)


def provider_list(request):
    context = {"base_template":"provider-base.html", 'active_menu': 'bookings', "active_header":"services"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
        context['user'] = user
    except Exception as e:
        pass
    return render(request, 'provider/provider-list.html', context=context)

def provider_details(request):
    context = {"base_template":"provider-base.html", "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
        context['user'] = user
    except Exception as e:
        pass
    return render(request, 'provider/provider-details.html', context=context)


def customer_booking(request):
    context = {"base_template":"base.html",  "active_menu": "bookings",
        "user_name": "John Smith1",
        "member_since": "Sep 2021", "active_header":"customers"}
    try:
        user_id = request.user_id
        context['user_type'] = User.objects.get(pk=user_id).user_type.user_type
        context['user'] = user
    except Exception as e:
        pass
    return render(request, 'customer/customer-booking.html', context=context)




