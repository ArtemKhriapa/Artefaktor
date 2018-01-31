from rest_framework import serializers
from apps.POI.models import POI, GisPOI
from rest_framework.validators import UniqueValidator


class POISerializer(serializers.ModelSerializer):

    class Meta:
        model = POI
        fields = (
            'lon',
            'lat',
            'description',
        )
    def validate(self, data):
        if not data.get('description') :
            raise serializers.ValidationError("Please enter description of this oject.")
        return data

class GisPOISerializer(serializers.ModelSerializer):
    class Meta:
        model = GisPOI
        fields = (
            'geometry', #exp
            'point',
            'polygon', #exp
        )
