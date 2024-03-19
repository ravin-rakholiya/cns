from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from service.models import *
from django.shortcuts import render, redirect
from .forms import ServicePostForm



def service_booking(request):
    context = {"base_template":"base.html",
        "user_name": "John Smith1",
        "member_since": "Sep 2021", "active_step":"appointment"}
    return render(request, 'services/service-booking.html', context=context)

def service_detail(request):
    context = {"base_template":"base.html",}
    return render(request, 'services/service-detail.html', context=context)

def service_payment(request):
    context = {"base_template":"base.html", "active_step":"payment"}
    return render(request, 'services/service-booking-payment.html', context=context)

def service_boooking_done(request):
    context = {"base_template":"base.html", "active_step":"done"}
    return render(request, 'services/service-booking-done.html', context=context)

def service_list(request):
    context = {"base_template":"base.html"}
    return render(request, 'services/service-list.html', context=context)

def service_create(request):
    context = {"base_template":"base.html"}
    if request.method == 'POST':
        form = ServicePostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = ServicePostForm()
    context['form'] = form
    return render(request, 'services/service-create.html', context=context)

