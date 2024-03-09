from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [

    path('', views.index, name='index'),

    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('provider_signup',views.provider_signup, name='provider_signup'),

path('choose_signup',views.choose_signup, name='choose_signup'),

    # path('generate_otp', views.GenerateOTP.as_view(), name='generate-otp'),
]
