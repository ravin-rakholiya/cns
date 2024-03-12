from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index_html'),  # Add this line

    path('user_signup', views.user_signup, name='user_signup'),
    path('Login_main', views.Login_main, name='Login_main'),
    path('choose_signup',views.choose_signup, name='choose_signup'),
    path('servicelist',views.servicelist, name='servicelist'),
    path('forgot_password',views.forgot_password, name='forgot_password'),
    path('password_recovery_success', views.password_recovery_success, name='password_recovery_success'),
    path('faq/', views.faq, name='faq'),
]
    # path('generate_otp', views.GenerateOTP.as_view(), name='generate-otp'),