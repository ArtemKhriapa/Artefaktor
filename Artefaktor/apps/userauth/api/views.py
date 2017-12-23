from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.shortcuts import HttpResponse
from apps.userauth.api.serializers import RegTrySerializer
from apps.extraapps.OTC.api.serializers  import OTCSerializer
from apps.userauth.models import RegistrarionTry
from apps.extraapps.OTC.models import OTCRegistration
from django.contrib.auth.models import User

class RegistrationTry(generics.CreateAPIView):
    queryset = RegistrarionTry.objects.all()
    serializer_class = RegTrySerializer
    
    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        print('here')
        # FOO BOO BL
        return res

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
    queryset = RegistrarionTry.objects.all()
    serializer_class = RegTrySerializer
    # response = "If you see this, then your registration completed successfully" # change to generics.API next time
    # return HttpResponse(response)

