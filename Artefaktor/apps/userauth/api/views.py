from django.http import Http404
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from apps.userauth.api.serializers import RegTrySerializer, SetPassSerialazer
from apps.extraapps.OTC.api.serializers  import OTCSerializer
from apps.userauth.models import RegistrationTry as RegistrationTryModel
from apps.extraapps.OTC.models import OTCRegistration

from django import forms
from django.core.mail import send_mail


class RegistrationTry(generics.CreateAPIView):
    queryset = RegistrationTryModel.objects.all()
    serializer_class = RegTrySerializer

    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        if res.status_code == status.HTTP_201_CREATED:
            pass
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
    serializer_class = OTCSerializer

    def get_object(self):
        #cheking OTC
        try:
            code = get_object_or_404(OTCRegistration, otc=self.kwargs.get('otc_check'))
            if not code.is_used :
                return code
            else:
                raise Http404
        except Exception as e:
            raise e # NOTICE: this is how we debug except blocks
            raise Http404


class SuccessRegistration(generics.ListCreateAPIView):
    queryset = RegistrationTryModel.objects.all()
    serializer_class = RegTrySerializer


class SetPass(generics.RetrieveAPIView,generics.CreateAPIView ):
    queryset = RegistrationTryModel.objects.all()
    serializer_class = SetPassSerialazer


    def get_object(self):
        #cheking OTC, cheking RegistrationTry
        try:
            code = get_object_or_404(OTCRegistration, otc=self.kwargs.get('otc_check'))
            registration = RegistrationTryModel.objects.get(otc=code.id)  # geting RegistrationTry by OTC
            if not code.is_used :
                return registration
            elif registration.is_finished:
                return registration
            else:
                print('404 in code.is_used')
                raise Http404
        except Exception as e:
            #raise e
            print('404 in get_object ---->', e)  # NOTICE: this is how we debug except blocks
            raise Http404

    def get_serializer(self, *args, **kwargs):
        #i d'nt now what is this((
        # maybe including 'context' in default serializer
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {
            #adding extra content in 'context'->>  RegTry from get_object
            'username': self.get_object().username,
            'email':self.get_object().email
        }
