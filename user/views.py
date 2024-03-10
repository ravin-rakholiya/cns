from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from service.models import Provider
from user.models import User, UserSignup, Login_main

from django.http import HttpResponseRedirect


# Create your views here.
def signup(request):
    if request.method == 'POST':
        # Process the signup form data here
        return HttpResponse('Signup successful!')
    else:
        return render(request, 'user/signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', False)

        user = Login_main(
            email=email,
            password=password,
            remember_me=remember_me,
        )
        user.save()

        return render(request, 'user/index.html')
    return render(request, 'user/index.html')


def index(request):
    return render(request, 'user/index.html')


def choose_signup(request):
    return render(request, 'choose_signup.html')


def user_signup(request):
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
        return render(request, 'user/signup.html')


def Login_main(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email and password match any user in UserSignup table
        try:
            user = UserSignup.objects.get(email=email)
        except UserSignup.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password):
            # User is found in UserSignup table, log them in
            # Implement your login logic here
            return redirect('user:index')

        # If user is not found in UserSignup table, check ProviderSignup table
        try:
            provider = Provider.objects.get(email=email)
        except Provider.DoesNotExist:
            provider = None

        if provider is not None and check_password(password, provider.password):
            # Provider is found in ProviderSignup table, log them in
            # Implement your login logic here
            return redirect('provider:index')

        # If neither user nor provider is found, show login error
        return render(request, 'user/Login_main.html', {'error': 'Invalid email or password'})

    return render(request, 'user/Login_main.html')

def servicehtml(request):
    return render(request, 'service/service_listing.html')
