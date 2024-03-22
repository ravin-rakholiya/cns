from django.urls import path, include
from service.views import *


app_name = 'service'

urlpatterns = [
    path('service-create', service_create, name='service_create'),
    path('service-detail', service_detail, name='service_detail'),
    path('service-booking', service_booking, name='service_booking'),
    path('service-payment', service_payment, name='service_payment'),
    path('service-booking-done', service_boooking_done, name='service_boooking_done'),
    path('service-list', ServiceListView.as_view(), name='service_list'),
]