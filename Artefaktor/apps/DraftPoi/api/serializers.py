from rest_framework import serializers
from apps.DraftPoi.models import DraftPoi

class DraftPoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPoi
        fields = (
            'submitted_by',
            'moderated_on',
            'accepted',
            'declined_reason',
        )

