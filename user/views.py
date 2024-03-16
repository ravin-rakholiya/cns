from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from cns import settings
from service.models import Provider
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

# Create your views here.
# def signup(request):
#     if request.method == 'POST':
#         # Process the signup form data here
#         return HttpResponse('Signup successful!')
#     else:
#         return render(request, 'user/signup.html')


# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         remember_me = request.POST.get('remember_me', False)

#         user = Login_main(
#             email=email,
#             password=password,
#             remember_me=remember_me,
#         )
#         user.save()

#         return render(request, 'user/index.html')
#     return render(request, 'user/index.html')





# def choose_signup(request):
#     return render(request, 'choose_signup.html')


# def user_signup(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         password = request.POST.get('password')

#         # Create a new User_s object and save it to the database

#         user = UserSignup(name=name, email=email, phone=phone, password=password)
#         user.save()

#         # Redirect the user to a different page after signup
#         return redirect('user:index')
#     else:
#         return render(request, 'user/signup.html')


# def Login_main(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Check if the email and password match any user in UserSignup table
#         try:
#             user = UserSignup.objects.get(email=email)
#         except UserSignup.DoesNotExist:
#             user = None

#         if user is not None and check_password(password, user.password):
#             # User is found in UserSignup table, log them in
#             # Implement your login logic here
#             return redirect('user:index')

#         # If user is not found in UserSignup table, check ProviderSignup table
#         try:
#             provider = Provider.objects.get(email=email)
#         except Provider.DoesNotExist:
#             provider = None

#         if provider is not None and check_password(password, provider.password):
#             # Provider is found in ProviderSignup table, log them in
#             # Implement your login logic here
#             return redirect('provider:index')

#         # If neither user nor provider is found, show login error
#         return render(request, 'user/Login_main.html', {'error': 'Invalid email or password'})

#     return render(request, 'user/Login_main.html')


# def servicelist(request):
#     return render(request, 'service/service_listing.html')


# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         user = User.objects.filter(email=email).first()

#         if user:
#             # Assuming you have a UserProfile model with a one-to-one relationship to User
#             user_profile, created = User.objects.get_or_create(user=user)

#             # Generate and store a reset token
#             token = user_profile.generate_reset_token()

#             # Send the reset link to the user's email
#             reset_link = f"{request.scheme}://{request.get_host()}/reset-password/?token={token}"
#             subject = 'Password Reset'
#             message = f'Click the following link to reset your password: {reset_link}'
#             from_email = settings.DEFAULT_FROM_EMAIL
#             to_email = [user.email]
#             send_mail(subject, message, from_email, to_email)

#             return render(request, 'user/password_recovery_success.html')

#     return render(request, 'user/password_recovery.html')


# def password_recovery_success(request):
#     return render(request, 'user/password_recovery_success.html')


# def faq(request):
#     # Your view logic here
#     return render(request, 'user/faq.html')
