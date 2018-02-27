from django.conf.urls import url
from apps.POI.api.views import ListGisPOIView, GisPOIView, NewGisPOIView, ListCategoryView

urlpatterns = [
    url(r'^$', ListGisPOIView.as_view()),
    # format : ?in_bbox={lat1,lon1,lat2,lon2}  - filter on two corner points(lat/lon)
    # format : ?dist={distance}&point={lat,lon} - filter in radius  on point(lat/lon) + distance in Km
    # format : ?name={}&description={} - filter on fields {name} and {description}
    # format : ?search={word} - search by {word}
    # format : ?cat={category},{category},{category}.... - filter on category
    #FIXME ?? isolated url for search?
    #FIXME ?? isolated url for filters?
    url(r'^cat/$',ListCategoryView.as_view()),
    # format : ?search={word} - search by {word} in name
    url(r'^id/(?P<POI_id>[0-9]+)/$', GisPOIView.as_view()),
    url(r'^new/$', NewGisPOIView.as_view())

]
