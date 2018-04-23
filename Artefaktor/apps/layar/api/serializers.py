from rest_framework import serializers
from apps.POI.models import GisPOI
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point

class Hotspots(serializers.ModelSerializer):
    # id = serializers.CharField(source='id')
    # aa = serializers.DictField
    class Meta:
        model = GisPOI
        fields = (
            'id',
            'anchor',
            'text',
        )

class LayarSerializer(serializers.Serializer):
    hotspots = Hotspots(read_only=True,many=True)
    layer = serializers.CharField(default = "No POI found. Please increase the search range to try again.")
    errorCode = serializers.IntegerField(default = 0)
    errorString = serializers.CharField(default = "Artefaktor")

