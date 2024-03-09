from django.shortcuts import render
from django.http import HttpResponse

from service.models import Provider
from user.models import User

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
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', False)
        login_with_otp = request.POST.get('login_with_otp', False)

        user = User.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            password=password,
            remember_me=remember_me,
            login_with_otp=login_with_otp
        )
        user.save()

        return render(request, 'user/login.html')
    return render(request, 'user/login.html')
def index(request):
    return render(request, 'user/index.html')
def choose_signup(request):
    return render(request, 'choose_signup.html')



def user_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        # Add more fields as needed

        user = User.objects.create(name=name, email=email)
        # Add more fields as needed

        return HttpResponseRedirect('/success')  # Redirect to a success page
    else:
        return render(request, 'user/signup.html')
def provider_signup(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            # Add more fields as needed

            provider = Provider.objects.create(name=name, email=email)
            # Add more fields as needed

            return HttpResponseRedirect('/success')  # Redirect to a success page
        else:
            return render(request, 'user/provider_signup.html')