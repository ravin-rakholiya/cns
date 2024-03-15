from django.urls import path, include
from user.views import *

app_name = 'user'

urlpatterns = [
    path('', index, name='index'),
    path('index', index, name='index_html'),  # Add this line
    path('choose_register', choose_register, name='choose_register'),  # Add this line
    path('provide_signup', provide_signup, name='provide_signup'),
    path('user_signup', user_signup, name='user_signup'),
    path('forgot_password', forgot_password, name='forgot_password'),
    path('reset_password', reset_password, name='reset_password'),

]
    # path('generate_otp', views.GenerateOTP.as_view(), name='generate-otp'),