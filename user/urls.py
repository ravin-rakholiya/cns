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
    # path('generate_otp', views.GenerateOTP.as_view(), name='generate-otp'),
]
