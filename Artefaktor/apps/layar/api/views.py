from rest_framework import generics
from apps.POI.models import GisPOI as GisPOI_model
from apps.filter.models import PointInRadiusFilter
from apps.layar.api.serializers import LayarSerializer

class LayarView(generics.RetrieveAPIView):
    # queryset = GisPOI_model.objects.all().order_by('id')
    serializer_class = LayarSerializer
    # pagination_class = CustomPagePagination
    # distance_filter_field = 'point'
    # distance_filter_convert_meters = True
    # distanc_filter_include_overlapping = True
    # filter_backends =(PointInRadiusFilter)

    def get_object(self):
        print('in view')
        return {
            'hotspots': GisPOI_model.objects.all().order_by('id'),
            'layer': 'hevie',
            'errorCode': 0,
            'errorString': 'some eerror'
        }