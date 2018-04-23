from rest_framework import serializers
from apps.extraapps.OTC.models import OTCRegistration


class OTCSerializer(serializers.ModelSerializer):

    class Meta:
        model = OTCRegistration
        fields = (
            'otc', 'created_in', 'is_used', 'used_in', 'link'
        )

