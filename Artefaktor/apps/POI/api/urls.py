from django.conf.urls import url
from apps.POI.api import views

urlpatterns = [
    url(r'^(?P<POI_id>[0-9])/$', views.POI.as_view()),
    url(r'^collection/$', views.POI.as_view())
]
