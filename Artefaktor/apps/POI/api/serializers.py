from rest_framework import serializers
from apps.POI.models import GisPOI, Category
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.gis.geos import Point
from rest_framework.validators import UniqueValidator

class ParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'name',
        )


class CategorySerializer(serializers.ModelSerializer):
    #parent = ParentSerializer()
    class Meta:
        model = Category
        fields = (
            'name',
            #'parent'
        )


class GisPOISerializer(GeoFeatureModelSerializer):
    tags = TagListSerializerField()
    category = CategorySerializer()
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
            'image',
            'tags',
            'category'
        )


class NewGisPOISerializer(TaggitSerializer,GeoFeatureModelSerializer):
    latitude = serializers.FloatField(write_only = True)
    longitude = serializers.FloatField(write_only = True)
    tags = TagListSerializerField()
    add_tags = serializers.CharField(write_only = True) # enter words separated by a coma+space
    category = CategorySerializer()
    class Meta:
        model = GisPOI
        geo_field = 'point'
        fields = (
            'name',
            'description',
            'addres',
            'radius',
            'add_tags',
            'tags',
            'latitude',
            'longitude',
            'category'
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
        # transformation lat/lon in point format
        point = Point(validated_data['latitude'], validated_data['longitude'] )
        newpoint = GisPOI.objects.create(
            name =validated_data.get('name'),
            point = point,
            description = validated_data['description'],
            addres = validated_data['addres'],
            radius = validated_data['radius'],

        )
        # adding tags
        for newtag in (validated_data['add_tags'].split(", ")):
            newpoint.tags.add(newtag)
        newpoint.save()
        return newpoint

