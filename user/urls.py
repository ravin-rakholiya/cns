from django.urls import path, include
from user.views import *

app_name = 'user'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('choose_register', ChooseRegisterView.as_view(), name='choose_register'),  # Add this line
    path('provider_signup', ProviderSignupView.as_view(), name='provide_signup'),
    
    path('verify_email', verifyEmail, name='verify_email'),

    path('user_signup', user_signup, name='user_signup'),
    path('forgot_password', forgot_password, name='forgot_password'),
    path('reset_password', reset_password, name='reset_password'),
    path('user_signin', user_signin, name='user_signin'),

    # Provider Routes
    path('provider-services', provider_services, name='provider_services'),
    path('provider-booking', provider_booking, name='provider_booking'),
    path('provider-list', provider_list, name='provider_list'),
    path('provider-details', provider_details, name='provider_details'),

    # customer Routes
    path('customer-booking', customer_booking, name='customer_booking'),
    path('customer_profile_creation', customer_profile_creation, name='customer_profile_creation'),

]