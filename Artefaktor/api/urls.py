from django.conf.urls import url, include



urlpatterns = [

    url(r'^registration/', include('apps.userauth.api.urls')),
    url(r'^POI/', include('apps.POI.api.urls')),
    url(r'^layar/', include('apps.layar.urls'))

]