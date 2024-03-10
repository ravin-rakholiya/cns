from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from service.models import Provider


# Create your views here.
def index(request):
    return render(request, 'service/index.html')


def provider_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Create a new Provider object and save it to the database
        provider = Provider(name=name, email=email, phone=phone, password=password)
        provider.save()

        # You might want to redirect the user to a different page after signup
        return redirect('user:index')

    return render(request, 'user/provider_signup.html')