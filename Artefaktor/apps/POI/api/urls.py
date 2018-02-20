from django.conf.urls import url
from apps.POI.api.views import *

urlpatterns = [
    url(r'^$', ListGisPOI.as_view()),
    # format : ?in_bbox={lat1,lon1,lat2,lon2}  - filter on two corner points(lat/lon)
    # format : ?dist={distance}&point={lat,lon} - filter in radius  on point(lat/lon) + distance in Km
    # format : ?name={}&description={} - filter on fields {name} and {description}
    # format : ?search={} - filter by {word}
    url(r'^id/(?P<POI_id>[0-9]+)/$', GisPOI.as_view()),
    # fixme: create isolated url for creating new POI

]
