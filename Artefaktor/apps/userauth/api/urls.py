from django.conf.urls import url
from apps.userauth.api import views

urlpatterns = [
    url(r'^$', views.Registration),
    url(r'^(?P<otc_check>[A-Za-z0-9]+)/$', views.RegistrationCheck.as_view()),
    url(r'^success/$', views.SuccessRegistration),

]