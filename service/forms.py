from django import forms
from .models import ServicePost, ServiceCategory


class ServicePostStep1Form(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=ServiceCategory.objects.all(), empty_label="Select Category")

    class Meta:
        model = ServicePost
        fields = ['title', 'category', 'price', 'duration', 'desc']
        labels = {
            'title' : 'Service Title',
            'category': 'Service Category',
            'price' : 'Service Price',
            'duration' : 'Service Duration',
            'desc' : 'Description'
        }
