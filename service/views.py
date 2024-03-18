from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from service.models import Provider
from django.shortcuts import render, redirect
from .forms import ServicePostStep1Form



# Create your views here.
def serviceindex(request):
    return render(request, 'servicebase.html')


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


#def create_service(request):
#    return render(request, 'create_service.html')


def create_service(request):
    if request.method == 'POST':
        form1 = ServicePostStep1Form(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form1 = ServicePostStep1Form()
    return render(request, 'create_service.html', {'form1': form1})
