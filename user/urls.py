from django.urls import path, include
from user.views import *

app_name = 'user'

urlpatterns = [
    path('', index, name='index'),
    path('index', index, name='index_html'),  # Add this line
    path('choose_register', choose_register, name='choose_register'),  # Add this line
    path('provide_signup', provide_signup, name='provide_signup'),
    path('user_signup', user_signup, name='user_signup'),
    path('forgot_password', ForgotPasswordPage.as_view(), name='forgot_password'),
    path('password_reset', PasswordResetView.as_view(), name='password_reset'),
]
    # path('generate_otp', views.GenerateOTP.as_view(), name='generate-otp'),