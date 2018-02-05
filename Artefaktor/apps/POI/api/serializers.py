from rest_framework import serializers
from apps.POI.models import GisPOI
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from django.contrib.gis.geos import Point
from rest_framework.validators import UniqueValidator


class GisPOISerializer(GeoFeatureModelSerializer):

    class Meta:
        model = GisPOI
        geo_field = 'point'
        fields = (
            'name',
            'description',
            'addres',
            'radius',
            'create_in',
            'created_was',
            'image'
        )


class NewGisPOISerializer(GeoFeatureModelSerializer):
    latitude = serializers.FloatField(write_only = True)
    longitude = serializers.FloatField(write_only = True)

    class Meta:
        model = GisPOI
        geo_field = 'point'
        fields = (
            'name',
            'description',
            'addres',
            'radius',
            'latitude',
            'longitude'
        )
    def validate(self, data):
        if not data.get('latitude') or not data.get('longitude'):
            raise serializers.ValidationError("Please enter the coordinates.")
        if data.get('latitude') > 90 or data.get('latitude') < -90:
            raise serializers.ValidationError("The latitude should be from -90 to 90 degrees.")
        if data.get('longitude') > 180 or data.get('longitude') < -180:
            raise serializers.ValidationError("The longitude should be from -180 to 180 degrees.")
        return data

    def create(self, validated_data):
        point = Point(validated_data['latitude'], validated_data['longitude'] ) # transformation lat/lon in point format
        newpoint = GisPOI.objects.create(
            name =validated_data.get('name'),
            point = point,
            description = validated_data['description'],
            addres = validated_data['addres'],
            radius = validated_data['radius'],
        )
        newpoint.save()
        return newpoint
