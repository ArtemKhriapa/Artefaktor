from django.conf.urls import url
from apps.POI.api.views import *

urlpatterns = [
    url(r'^inradius/(?P<lat>[0-9.-]+)\@(?P<lon>[0-9.-]+)\km(?P<radius_km>[0-9.]{1,3})/$', RadiusGisPOI.as_view()),
    #FIXME: need to check the length of coordinates
    url(r'^$', NewGisPOI.as_view()),
    url(r'^id/(?P<POI_id>[0-9]+)/$', GisPOI.as_view()),

]
