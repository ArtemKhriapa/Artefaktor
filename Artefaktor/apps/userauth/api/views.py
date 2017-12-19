from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from apps.userauth.api.serializers import OTCSerializer
from django.shortcuts import HttpResponse
from apps.extraapps.OTC.models import OTCRegistration

def Registration(request):
    response = "If you see this, then you are in the process of registering"
    return HttpResponse(response)

class RegistrationCheck(generics.RetrieveUpdateAPIView):
    queryset = OTCRegistration.objects.all()
    serializer_class = OTCSerializer

    def get_object(self):
        
        code = get_object_or_404(OTCRegistration, otc=self.kwargs.get('otc_check'))
        return code

def SuccessRegistration(request):
    response = "If you see this, then your registration completed successfully"
    return HttpResponse(response)

