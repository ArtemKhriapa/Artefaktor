from rest_framework import serializers
from apps.POI.models import GisPOI #POI,
from rest_framework.validators import UniqueValidator


class GisPOISerializer(serializers.ModelSerializer):

    class Meta:
        model = GisPOI
        fields = (
            'description',
            'point',
        )

class NewGisPOISerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only = True )
    longitude = serializers.FloatField(write_only = True)

    class Meta:
        model = GisPOI
        fields = (
            'description',
            'latitude',
            'longitude',
        )

    def validate(self, data):
        if not data.get('latitude') or not data.get('longitude'):
            raise serializers.ValidationError("Please enter the coordinates")
        if data.get('latitude') > 90 or data.get('latitude') < -90:
            raise serializers.ValidationError("The latitude should be from -90 to 90 degrees")
        if data.get('longitude') > 180 or data.get('longitude') < -180:
            raise serializers.ValidationError("The longitude should be from -180 to 180 degrees")
        if not data.get('description'):
            raise serializers.ValidationError("Please enter description of this oject.")
        return data

    def create(self, validated_data):
        point = 'SRID=4326;POINT ('+ str(validated_data['longitude']) +' '+ str(validated_data['latitude'])+')'
        newpoint = GisPOI.objects.create(point = point, description = validated_data['description'])
        print(point)
        newpoint.save()

        return newpoint