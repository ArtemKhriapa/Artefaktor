from rest_framework import serializers
from apps.POI.models import GisPOI, Category
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.gis.geos import Point
from rest_framework.validators import UniqueValidator


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
    category = CategorySerializer(read_only=True, many=True)
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


class NewGisPOISerializer(GeoFeatureModelSerializer): #TaggitSerializer,
    latitude = serializers.FloatField(write_only = True)
    longitude = serializers.FloatField(write_only = True)
    tags = TagListSerializerField()
    add_tags = serializers.CharField(write_only = True) # enter words separated by a coma+space
    #add_category = serializers.CharField(write_only = True)

    class Meta:
        model = GisPOI
        geo_field = 'point'
        fields = (
            'id',
            'name',
            'description',
            'addres',
            'radius',
            'add_tags',
            'tags',
            'latitude',
            'longitude',
            #'add_category',
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
        point = Point(validated_data['latitude'], validated_data['longitude'])
        newpoint = GisPOI.objects.create(
            name =validated_data.get('name'),
            point = point,
            description = validated_data['description'],
            addres = validated_data['addres'],
            radius = validated_data['radius'],
        )
        newpoint.save()
        #adding tags
        for newtag in (validated_data['add_tags'].split(",")):
            newpoint.tags.add(newtag)
        #adding category
        #try:
            # print('valid:', validated_data['category'])
            # newcategory_set = Category.objects.filter(validated_data['category'])
            # print('set: ', newcategory_set)
        # newcategory = Category.objects.get(name = validated_data['add_category'])
        for category in validated_data['category']:
            newpoint.category.add(category)
        newpoint.save()
        #except Exception as e:
            # print(e)
            #raise serializers.ValidationError("Wrong categoty!")  # why it rise not dict???

        newpoint.save()
        return newpoint


class ListGisPOISerializer(TaggitSerializer,GeoFeatureModelSerializer):
    latitude = serializers.FloatField(write_only = True)
    longitude = serializers.FloatField(write_only = True)
    tags = TagListSerializerField()
    add_tags = serializers.CharField(write_only = True) # enter words separated by a coma+space
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = GisPOI
        geo_field = 'point'
        fields = (
            'id',
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


