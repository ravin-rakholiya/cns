from django.http import HttpResponseRedirect
from django.shortcuts import render

from service.models import Provider


# Create your views here.
def index(request):
    return render(request, 'service/index.html')
