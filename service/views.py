from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
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
        context['user'] = user
    except Exception as e:
        pass
    return render(request, 'services/service-booking.html', context=context)

class ServiceDetailView(View):
    template_name = 'services/service-detail.html'
    base_template = 'base.html'

    def get(self, request, provider_service):
        context = {'base_template': self.base_template}
        try:
            user = User.objects.get(pk=request.user_id)
            context['user_type'] = user.user_type.user_type
            context['user'] = user
            provider_service = ProviderService.objects.get(pk = provider_service)
            service_availability = ProviderAvailability.objects.filter(service = provider_service)
            context['provider_service'] = provider_service
            context['service_availability'] = service_availability
        except Exception as e:
            pass
        return render(request, self.template_name, context=context)

def service_payment(request):
    context = {"base_template":"base.html", "active_step":"payment", "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
        context['user'] = user
    except Exception as e:
        pass
    return render(request, 'services/service-booking-payment.html', context=context)

def service_boooking_done(request):
    context = {"base_template":"base.html", "active_step":"done", "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
        context['user'] = user
    except Exception as e:
        pass
    return render(request, 'services/service-booking-done.html', context=context)

class ServiceListView(View):
    template_name = 'services/service-list.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        context = {"base_template":self.base_template, "active_header":"providers"}
        try:
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            context['user_type'] = user.user_type.user_type
            provider_services = ProviderService.objects.filter(provider = user)
            context['provider_services'] = provider_services
            context['user'] = user
        except Exception as e:
            return redirect('user:user_signin')
        return render(request, self.template_name, context=context)



def service_create(request):
    context = {"base_template":"base.html", "active_header":"providers"}
    try:
        user = User.objects.get(pk=request.user_id)
        context['user_type'] = user.user_type.user_type
        context['user'] = user
    except Exception as e:
        pass
    return render(request, 'services/service-create.html', context=context)

