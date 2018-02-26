from django.conf.urls import url
from apps.POI.api.views import ListGisPOI, GisPOI, NewGisPOI

urlpatterns = [
    url(r'^$', ListGisPOI.as_view()),
    # format : ?in_bbox={lat1,lon1,lat2,lon2}  - filter on two corner points(lat/lon)
    # format : ?dist={distance}&point={lat,lon} - filter in radius  on point(lat/lon) + distance in Km
    # format : ?name={}&description={} - filter on fields {name} and {description}
    # format : ?search={word} - filter by {word}
    # format : ?cat={category},{category},{category}.... - filter on category
    # ?? isolated url for search? 
    # ?? isolated url for filters? 
    url(r'^id/(?P<POI_id>[0-9]+)/$', GisPOI.as_view()),
    url(r'^new/$', NewGisPOI.as_view())

]
