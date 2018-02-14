from django.conf.urls import url
from apps.POI.api.views import *

urlpatterns = [
    url(r'^$', ListGisPOI.as_view()),
    # format : ?in_bbox=lat1,lon1,lat2,lon2  - filter on two corner points(lat/lon)
    # format : ?dist=111&point=39.0,40.0 - filter on point(lat/lon) + distance in Km
    url(r'^id/(?P<POI_id>[0-9]+)/$', GisPOI.as_view()),

]
