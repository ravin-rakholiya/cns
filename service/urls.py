from django.urls import path, include
from service import views
from . import  views


app_name = 'service'

urlpatterns = [
    path('index/', views.index, name='index')


	# path('generate_otp', views.GenerateOTP.as_view(), name='generate-otp'),
]