from django.conf.urls import url
from apps.POI.api.views import *

urlpatterns = [
    url(r'^$', NewGisPOI.as_view()),
    # format : ?in_bbox=lat1,lon1,lat2,lon2  - filter on two corner points
    # format :
    url(r'^id/(?P<POI_id>[0-9]+)/$', GisPOI.as_view()),

]
