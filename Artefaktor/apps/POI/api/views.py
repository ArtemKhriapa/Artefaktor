from rest_framework import generics, status, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import Distance
from rest_framework.pagination import PageNumberPagination
from apps.POI.api.serializers  import  GisPOISerializer, NewGisPOISerializer
from apps.POI.models import GisPOI as GisPOI_model
from rest_framework_gis.filters import InBBoxFilter, DistanceToPointFilter


class CustomPagePagination(PageNumberPagination):
    #class for set pagination parameters
    page_size = 4 #obj in page
    page_size_query_param = 'page_size'
    max_page_size = 7

class PointInRadiusFilter(DistanceToPointFilter):
    # find all POI in radius
    def get_queryset(self, request):#, queryset, view
        dist = request.query_params.get(self.dist_param)
        point = self.get_filter_point(request)
        return GisPOI_model.objects.filter(point__distance_lte=(point, Distance(km=dist) ))



class ListGisPOI(generics.ListCreateAPIView):
    queryset = GisPOI_model.objects.all()
    serializer_class = NewGisPOISerializer
    pagination_class = CustomPagePagination
    bbox_filter_field = 'point'
    distance_filter_field = 'point'
    distance_filter_convert_meters = True
    bbox_filter_include_overlapping = True
    distanc_filter_include_overlapping = True
    filter_backends =(DjangoFilterBackend, filters.SearchFilter, InBBoxFilter, PointInRadiusFilter)#
    filter_fields = ('name','description') # filter with 100% match in fields ?
    search_fields = ('name','description', 'addres') #search partial match in all of this fields ?


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


# class RadiusGisPOI(generics.ListCreateAPIView):
#     serializer_class = GisPOISerializer
#
#     def get_queryset(self,*args, **kwargs):
#         point = Point(float(self.kwargs.get('lat')), float(self.kwargs.get('lon')))
#         pnt = GEOSGeometry(point,srid=4326 )
#         return GisPOI_model.objects.filter(point__distance_lte=(pnt, Distance(km=self.kwargs.get('radius_km'))))