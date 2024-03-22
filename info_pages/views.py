from django.shortcuts import render
from django.views import View
from user.models import User

# Create your views here.

class AboutUsView(View):
    template_name = 'aboutus/about-us.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        context = {"base_template":self.base_template, "active_header":"about"}
        try:
            user_id = request.user_id
            context['user_type'] = User.objects.get(pk=user_id).user_type.user_type
        except Exception as e:
            pass
        return render(request, self.template_name, context=context)


class ContactUsView(View):
    template_name = 'contactus/contact-us.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        context = {"base_template":"base.html", "active_header":"contactus"}
        try:
            user_id = request.user_id
            context['user_type'] = User.objects.get(pk=user_id).user_type.user_type
        except Exception as e:
            pass
        return render(request, self.template_name, context=context)

class PrivacyPolicyView(View):
    template_name = 'privacypolicy/privacy-policy.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        context = {"base_template":"base.html"}
        try:
            user_id = request.user_id
            context['user_type'] = User.objects.get(pk=user_id).user_type.user_type
        except Exception as e:
            pass
        return render(request, self.template_name, context=context)

class TermsAndConditionsView(View):
    template_name = 'termsncondition/terms-and-condition.html'
    base_template = 'base.html'

    def get(self, request, *args, **kwargs):
        context = {"base_template":"base.html"}
        try:
            user_id = request.user_id
            context['user_type'] = User.objects.get(pk=user_id).user_type.user_type
        except Exception as e:
            pass
        return render(request, self.template_name, context=context)