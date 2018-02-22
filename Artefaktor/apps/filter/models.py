from rest_framework_gis.filters import DistanceToPointFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.POI.models import GisPOI as GisPOI_model
from django.contrib.gis.measure import Distance

class PointInRadiusFilter(DistanceToPointFilter):     
    # find all POI in radius
    def filter_queryset(self, request, queryset, view):
        if ('point' and 'dist') in request.GET :
            # only if 'point' and 'dist' in request call this filter
            # without this enother filters not working, only PointInRadiusFilter
            dist = request.query_params.get(self.dist_param)
            point = self.get_filter_point(request)
            return GisPOI_model.objects.filter(point__distance_lte=(point, Distance(km=dist)))
        else:
            return queryset


class CategoryFilter(DjangoFilterBackend):
    #find all POI in category 
    pass
