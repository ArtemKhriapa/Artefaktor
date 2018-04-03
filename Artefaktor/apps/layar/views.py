from rest_framework import generics
from apps.POI.models import GisPOI as GisPOI_model
from apps.filter.models import PointInRadiusFilter

class LayarView(generics.ListAPIView):
    queryset = GisPOI_model.objects.all().order_by('id') # sorted by id ?
    # serializer_class = ListGisPOISerializer
    # pagination_class = CustomPagePagination
    distance_filter_field = 'point'
    distance_filter_convert_meters = True
    distanc_filter_include_overlapping = True
    filter_backends =(PointInRadiusFilter)