from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from service.models import *
from django.shortcuts import render, redirect
from service.forms import ServicePostForm
from user.models import *
from service.forms import *

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
    form_class = SearchForm

    def get(self, request, *args, **kwargs):
        context = {"base_template":self.base_template, "active_header":"providers"}
        try:
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            context['user_type'] = user.user_type.user_type
            if user.user_type.user_type == 'provider':
                provider_services = ProviderService.objects.filter(provider = user)
            else:
                provider_services = ProviderService.objects.all()
            service_ratings_data = {}
            for service in provider_services:
                service_ratings_data[service.id] = 0
                bookings = ServiceBooking.objects.filter(service = service)
                total_ratings = 0
                service_ratings_length = 1
                for booking in bookings:
                    service_ratings = ServiceRating.objects.filter(service=booking)
                    service_ratings_length = service_ratings_length+len(service_ratings)
                    for service_rate in service_ratings:
                        total_ratings = total_ratings+service_rate.rate
                if total_ratings != 0 or total_ratings != 0.0:
                    service_ratings_data[service.id] = round(total_ratings/service_ratings_length,1)
            context['provider_services'] = provider_services
            context['user'] = user
            context['service_ratings'] = service_ratings_data
            context['form'] = self.form_class()
        except Exception as e:
            print("89-----",e)
            return redirect('user:user_signin')
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = {"base_template":self.base_template, "active_header":"providers"}
        form = self.form_class(request.POST)
        context['form'] = self.form_class()
        if form.is_valid():
            search_input = form.cleaned_data.get('search_input')
            user_id = request.user_id
            user = User.objects.get(pk = user_id)
            context['user_type'] = user.user_type.user_type
            if search_input != '':
                if user.user_type.user_type == 'provider':
                    provider_services = ProviderService.objects.filter(provider = user, title__contains = search_input)
                else:
                    provider_services = ProviderService.objects.filter(title__contains = search_input)
            else:
                provider_services = ProviderService.objects.filter(provider = user)
            service_ratings_data = {}
            for service in provider_services:
                service_ratings_data[service.id] = 0
                bookings = ServiceBooking.objects.filter(service = service)
                total_ratings = 0
                service_ratings_length = 1
                for booking in bookings:
                    service_ratings = ServiceRating.objects.filter(service=booking)
                    service_ratings_length = service_ratings_length+len(service_ratings)
                    for service_rate in service_ratings:
                        total_ratings = total_ratings+service_rate.rate
                if total_ratings != 0 or total_ratings != 0.0:
                    service_ratings_data[service.id] = round(total_ratings/service_ratings_length,1)
            context['provider_services'] = provider_services
            context['user'] = user
            context['service_ratings'] = service_ratings_data
            context['search_input'] = search_input
            return render(request, self.template_name, context=context)
        else:
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

