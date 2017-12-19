from django.shortcuts import get_object_or_404
from rest_framework import generics
from apps.extraapps.OTC.api.serializers import OTCSerializer
from apps.extraapps.OTC.models import OTCRegistration

class CreateOTC(generics.CreateAPIView):
    queryset = OTCRegistration.objects.all()
    serializer_class = OTCSerializer


    # def perform_create(self, OTCSerializer):
    #     serializer.save(self)                         #how create new OTC in RegistrationTry ??