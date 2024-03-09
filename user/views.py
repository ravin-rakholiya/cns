from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def signup(request):
    return render(request, 'user/signup.html')


def index(request):
    return render(request, 'user/index.html')
