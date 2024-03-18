from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from service.models import Provider


def service_booking(request):
    context = {"base_template":"base.html",
        "user_name": "John Smith1",
        "member_since": "Sep 2021", "active_step":"appointment"}
    return render(request, 'services/service-booking.html', context=context)

def service_payment(request):
    context = {"base_template":"base.html", "active_step":"payment"}
    return render(request, 'services/service-booking-payment.html', context=context)

def service_boooking_done(request):
    context = {"base_template":"base.html", "active_step":"done"}
    return render(request, 'services/service-booking-done.html', context=context)

