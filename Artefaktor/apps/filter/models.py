from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework.filters import BaseFilterBackend
from apps.POI.models import GisPOI , Category
from django.contrib.gis.measure import Distance

class PointInRadiusFilter(DistanceToPointFilter):     
    # find all POI in radius
    def filter_queryset(self, request, queryset, view):
        if ('point' and 'dist') in request.GET :
            # only if 'point' and 'dist' in request call this filter
            # without this enother filters not working, only PointInRadiusFilter
            dist = request.query_params.get(self.dist_param)
            point = self.get_filter_point(request)
            return GisPOI.objects.filter(point__distance_lte=(point, Distance(km=dist)))
        else:
            return queryset


class CategoryFilter(BaseFilterBackend):
    #find all POI in category
    cat_param = 'cat'

    def get_filter_cat(self, request):
        cat_string = request.query_params.get(self.cat_param, None)
        if not cat_string:
            return None
        else:
            return cat_string.split(',')

    def filter_queryset(self, request, queryset, view):
        if 'cat' in request.GET :
            print('you ask me about: ',self.get_filter_cat(request))
            try:
                q = Category.objects.get(name =self.get_filter_cat(request) ).get_descendants(include_self=True)
                return q
            except Exception as e:
                return queryset
        else:
            return queryset


        #
        #
        #
        # if 'cat' in request.GET :
        #
        #
        #     return queryset
