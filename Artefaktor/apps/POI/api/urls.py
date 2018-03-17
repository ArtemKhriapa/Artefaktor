from django.conf.urls import url
from apps.POI.api.views import ListGisPOIView, GisPOIView, NewDraftGisPOIView, ListCategoryView, GisPOIESView

urlpatterns = [
    url(r'^$', ListGisPOIView.as_view()),
    # format : ?in_bbox={lat1,lon1,lat2,lon2}  - filter on two corner points(lat/lon)
    # format : ?dist={distance}&point={lat,lon} - filter in radius  on point(lat/lon) + distance in Km
    # format : ?name={}&description={} - filter on fields {name} and {description}
    # format : ?search={word} - search by {word}
    # format : ?cat={slug},{slug},{slug}.... - filter on category by slug (Category filter)
    url(r'^esearch/$', GisPOIESView.as_view()), # with ElasticSearch
    # format :
    url(r'^cat/$',ListCategoryView.as_view()),
    # format : ?search={word} - search by {word} in name
    url(r'^id/(?P<POI_id>[0-9]+)/$', GisPOIView.as_view()),
    url(r'^new/$', NewDraftGisPOIView.as_view()) # create new DraftGisPoi

]
