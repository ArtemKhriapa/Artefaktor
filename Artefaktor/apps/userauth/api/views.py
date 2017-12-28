from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
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
    queryset = RegistrationTryModel.objects.all()
    serializer_class = RegTrySerializer

    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        if res.status_code == status.HTTP_201_CREATED:
            print('here')
            '''
            TODO: Move to signal trough mailer app
            send_mail(
                'Please verify your account',
                message = render_to_string('Templates.html', {'foo': 'bar'}),
                to = User.user_email
            )
            '''
        return res


class RegistrationCheck(generics.RetrieveUpdateAPIView):
    queryset = OTCRegistration.objects.all()
    serializer_class = OTCSerializer # only for view, change next time ??

    def get_object(self):
        try:
            code = get_object_or_404(OTCRegistration, otc=self.kwargs.get('otc_check'))
            # FIXME: check unused registration
            
            registration = RegistrationTryModel.objects.get(otc = code)            ## problems
            registration.finishing()                                           ## problems
            return code
        except Exception as e:
            #raise e # NOTICE: this is how we debug except blocks
            raise Http404


class SuccessRegistration(generics.ListAPIView):
    queryset = RegistrationTryModel.objects.all()
    serializer_class = RegTrySerializer


