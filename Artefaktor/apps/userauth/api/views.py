from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from apps.userauth.api.serializers import OTCSerializer
from django.shortcuts import HttpResponse
from apps.extraapps.OTC.models import OTC

def Registration(request):
    response = "If you see this, then you are in the process of registering"
    return HttpResponse(response)

class RegistrationCheck(generics.RetrieveUpdateAPIView):
    queryset = OTC.objects.all()
    serializer_class = OTCSerializer

    def get_object(self):
        print('h1')
        print(self.kwargs.get('otc_check'))
        print(OTC.objects.all())
        for o in OTC.objects.all():
            print(o.otc==self.kwargs.get('otc_check'))
        print('_'*100)
        
        code = get_object_or_404(OTC, otc=self.kwargs.get('otc_check'))
        print('hhh')
        return code

def SuccessRegistration(request):
    response = "If you see this, then your registration completed successfully"
    return HttpResponse(response)

