from django import forms
from django.contrib.auth.forms import PasswordResetForm

from service.models import Provider
from user.models import User



class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class ProviderSignupForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'johndoe@example.com'}))
