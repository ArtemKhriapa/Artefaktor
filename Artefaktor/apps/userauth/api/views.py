from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.shortcuts import HttpResponse
from apps.userauth.api.serializers import OTCSerializer, RegTrySerializer
from apps.userauth.models import RegistrarionTry

from apps.extraapps.OTC.models import OTCRegistration

class RegistrationTry(generics.CreateAPIView):
    queryset = RegistrarionTry.objects.all()
    serializer_class = RegTrySerializer


class RegistrationCheck(generics.RetrieveUpdateAPIView):
    queryset = OTCRegistration.objects.all()
    serializer_class = OTCSerializer # only for view, change next time

    def get_object(self):
        code = get_object_or_404(OTCRegistration, otc=self.kwargs.get('otc_check'))
        return code

def SuccessRegistration(request):
    response = "If you see this, then your registration completed successfully"
    return HttpResponse(response)

