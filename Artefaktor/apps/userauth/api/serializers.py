from rest_framework import serializers
from apps.extraapps.OTC.models import OTC


class OTCSerializer(serializers.ModelSerializer):

    class Meta:
        model = OTC
        fields = (
            'otc', 'is_used'
        )
