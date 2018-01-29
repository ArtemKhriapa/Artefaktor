from django.http import Http404
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from apps.POI.api.serializers  import POISerializer
from apps.POI.models import POI as POI_model
from django import forms
from django.core.mail import send_mail


class POI(generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = POI_model.objects.all()
    serializer_class = POISerializer

    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        if res.status_code == status.HTTP_201_CREATED:
            pass
        return res

    def get_object(self):
        try:
            poi = get_object_or_404(POI_model, id=self.kwargs.get('POI_id'))
            return poi
        except Exception as e:
            print(e)
            raise Http404

'''class SuccessRegistration(generics.ListCreateAPIView):
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


def HomeView(request):
    #response = "Welcome home!"
    return render(request, 'home.html')
    #return HttpResponse(response)'''