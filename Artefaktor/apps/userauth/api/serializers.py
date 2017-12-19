from rest_framework import serializers
from apps.extraapps.OTC.models import OTCRegistration
from apps.userauth.models import RegistrarionTry

class OTCSerializer(serializers.ModelSerializer):

    class Meta:
        model = OTCRegistration
        fields = (
            'otc', 'created_in', 'is_used', 'used_in' , 'link'
        )

class RegTrySerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistrarionTry
        fields = (
            'id',
            'registrationtext'
        )