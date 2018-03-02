from django.conf.urls import url
from apps.DraftPoi.views import NewDraftPoi,DeleteDraftPoi


urlpatterns = [
    url(r'^$', NewDraftPoi.as_view()),
    url(r'^id/(?P<POI_id>[0-9]+)/$',DeleteDraftPoi.as_view()),
]