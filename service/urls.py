from django.urls import path, include
from service import views
from service.views import *


app_name = 'service'

urlpatterns = [
    path('service-booking', service_booking, name='service_booking'),
    path('service-payment', service_payment, name='service_payment'),
    path('service-booking-done', service_boooking_done, name='service_boooking_done'),
]