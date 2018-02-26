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
        # get list categories
        cat_string = request.query_params.get(self.cat_param, None)
        if not cat_string:
            return None
        else:
            return cat_string.split(',')

    def filter_queryset(self, request, queryset, view):
        if 'cat' in request.GET :
            try:
                # get set category
                category_set = Category.objects.filter(name__in = self.get_filter_cat(request))
                # get descendants of the object (include self)
                descendants = category_set.get_descendants(include_self=True)
                # get POIs from set of descendants
                point_set = GisPOI.objects.filter(category__in = descendants)
                # removing duplicates if POI associated with many categories
                sort_point_set = []
                for point in point_set:
                    if point not in sort_point_set:
                        sort_point_set.append(point)
                return sort_point_set

            except Exception as e:
                #print(e)
                return queryset
        else:
            return queryset
