from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from service.models import *
from django.shortcuts import render, redirect
from service.forms import ServicePostForm
from user.models import *


def service_booking(request):
    context = {"base_template":"base.html",
        "user_name": "John Smith1",
        "member_since": "Sep 2021", "active_step":"appointment"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
    except Exception as e:
        pass
    return render(request, 'services/service-booking.html', context=context)

def service_detail(request):
    context = {"base_template":"base.html",}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
    except Exception as e:
        pass
    return render(request, 'services/service-detail.html', context=context)

def service_payment(request):
    context = {"base_template":"base.html", "active_step":"payment", "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
    except Exception as e:
        pass
    return render(request, 'services/service-booking-payment.html', context=context)

def service_boooking_done(request):
    context = {"base_template":"base.html", "active_step":"done", "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
    except Exception as e:
        pass
    return render(request, 'services/service-booking-done.html', context=context)

def service_list(request):
    context = {"base_template":"base.html", "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
    except Exception as e:
        pass
    return render(request, 'services/service-list.html', context=context)

def service_create(request):
    context = {"base_template":"base.html", "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
    except Exception as e:
        pass
    return render(request, 'services/service-create.html', context=context)

