from django import forms
from .models import ServicePost, ServiceCategory
from user.models import UserType

class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = ServicePost
        fields = ['category', 'user', 'desc', 'per_hrs_rate', 'hrs_of_work', 'created_at', 'updated_at']
        category = forms.ModelChoiceField(
            queryset=ServiceCategory.objects.all(),
            empty_label='Select Service Category'
        ),
        user = forms.CharField(initial=UserType.user_type)
        labels = {
            'user': 'User Type',
            'category': 'Service Category',
            'desc': 'Service Description',
            'per_hrs_rate': 'Per hour Rate of Work',
            'hrs_of_work': 'Available hours per week',
            'created_at': 'Creation Date',
            'Updated at': 'Updated Date'
        }
