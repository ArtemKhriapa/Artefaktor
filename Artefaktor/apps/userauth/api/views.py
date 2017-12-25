from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from apps.userauth.api.serializers import RegTrySerializer
from apps.extraapps.OTC.api.serializers  import OTCSerializer
from apps.userauth.models import RegistrationTry as RegistrationTryModel
from apps.extraapps.OTC.models import OTCRegistration
from django.contrib.auth.models import User
from django import forms
from django.core.mail import send_mail


class RegistrationTry(generics.CreateAPIView):
    queryset = RegistrationTryModel.objects.all()# FIXME: registraTION!
    serializer_class = RegTrySerializer

    def signup(request):
        if request.method == 'POST':
            forms = RegistrationTryModel(forms.Form)
            if forms.is_valid():
                User.save()
            send_mail(
                'Please verify your account',
                message = render_to_string('Templates.html', {'foo': 'bar'}),
                to = User.user_email
            )


class RegistrationCheck(generics.RetrieveUpdateAPIView):
    queryset = OTCRegistration.objects.all()
    serializer_class = OTCSerializer # only for view, change next time

    def get_object(self):
        try:
            code = get_object_or_404(OTCRegistration, otc=self.kwargs.get('otc_check'))
            return code
        except:
            raise Http404


class SuccessRegistration(generics.ListAPIView):
    queryset = RegistrationTryModel.objects.all()
    serializer_class = RegTrySerializer
    # response = "If you see this, then your registration completed successfully" # change to generics.API next time
    # return HttpResponse(response)

