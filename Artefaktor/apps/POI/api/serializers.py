from rest_framework import serializers
from apps.POI.models import GisPOI
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from django.contrib.gis.geos import Point
from rest_framework.validators import UniqueValidator


class GisPOISerializer(serializers.ModelSerializer):

    class Meta:
        model = GisPOI
        fields = (
            'name',
            'description',
            'point',
            'create_in',
            'created_was',
            'image'
        )
#Fixme : ned to fix!
'''
class NewGisPOISerializer(GeoFeatureModelSerializer,serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    calc_point = GeometrySerializerMethodField() #method calculate Point from lat/lon

    class Meta:
        model = GisPOI
        geo_field = 'calc_point'
        fields = (
            'name',
            'description',
            'point',
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

    def get_calc_point(self, validated_data):
        return Point(validated_data['latitude'],validated_data['longitude'] )

    def create(self, validated_data):
        point = Point
        newpoint = GisPOI.objects.create(point = Point, description = validated_data['description'])
        print(point)
        newpoint.save()

        return newpoint
        '''

class NewGisPOISerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only = True)
    longitude = serializers.FloatField(write_only = True)

    class Meta:
        model = GisPOI
        fields = (
            'name',
            'description',
            'latitude',
            'longitude',
        )

    def validate(self, data):
        if not data.get('latitude') or not data.get('longitude'):
            raise serializers.ValidationError("Please enter the coordinates.")
        if data.get('latitude') > 90 or data.get('latitude') < -90:
            raise serializers.ValidationError("The latitude should be from -90 to 90 degrees.")
        if data.get('longitude') > 180 or data.get('longitude') < -180:
            raise serializers.ValidationError("The longitude should be from -180 to 180 degrees.")
        if not data.get('description'):
            raise serializers.ValidationError("Please enter description of this oject.")
        if not data.get('name'):
            raise serializers.ValidationError("Please enter the name.")
        return data

    def create(self, validated_data):
        point = 'SRID=4326;POINT ('+ str(validated_data['longitude']) +' '+ str(validated_data['latitude'])+')'
        newpoint = GisPOI.objects.create(point = point, description = validated_data['description'])
        print(point)
        newpoint.save()

        return newpoint