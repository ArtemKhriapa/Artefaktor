from django.http import Http404
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import Distance

from apps.POI.api.serializers  import  GisPOISerializer, NewGisPOISerializer
from apps.POI.models import GisPOI as GisPOI_model


class NewGisPOI(generics.CreateAPIView):
    serializer_class = NewGisPOISerializer
    model = GisPOI_model

    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        res.status_code == status.HTTP_201_CREATED
        return res


class GisPOI(generics.RetrieveAPIView):
    queryset = GisPOI_model.objects.all()
    serializer_class = GisPOISerializer

    def get_object(self):
        return get_object_or_404(GisPOI_model, id=self.kwargs.get('POI_id'))


class RadiusGisPOI(generics.ListCreateAPIView):
    serializer_class = GisPOISerializer

    def get_queryset(self,*args, **kwargs):
        point = Point(float(self.kwargs.get('lat')), float(self.kwargs.get('lon')))
        pnt = GEOSGeometry(point,srid=4326 )
        return GisPOI_model.objects.filter(point__distance_lte=(pnt, Distance(km=self.kwargs.get('radius_km'))))