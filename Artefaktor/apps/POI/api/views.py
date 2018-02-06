from django.http import Http404
from rest_framework import generics, status, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import Distance
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from apps.POI.api.serializers  import  GisPOISerializer, NewGisPOISerializer
from apps.POI.models import GisPOI as GisPOI_model


class CustomPagePagination(PageNumberPagination):
    #class for set pagination parameters
    page_size = 4 #obj in page
    page_size_query_param = 'page_size'
    max_page_size = 100000




class NewGisPOI(generics.ListCreateAPIView):
    queryset = GisPOI_model.objects.all()
    serializer_class = NewGisPOISerializer
    pagination_class = CustomPagePagination
    #model = GisPOI_model
    filter_backends =(DjangoFilterBackend, filters.SearchFilter) #
    filter_fields = ('name', 'addres','description','point') # sfilter with 100% match in fields
    search_fields = ('name','description', 'addres') #search partial match in fields


    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        res.status_code == status.HTTP_201_CREATED
        return res

    def get_queryset(self, *args, **kwargs):
        return GisPOI_model.objects.all()

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