from django.conf.urls import url
from apps.userauth.api import views

urlpatterns = [
    url(r'^$', views.RegistrationTry.as_view()),
    url(r'^(?P<otc_check>[a-f0-9-]{36})/$', views.RegistrationCheck.as_view()),
    url(r'^(?P<otc_check>[a-f0-9-]{36})/set_password/$', views.SetPass.as_view()),
    url(r'^success/$', views.SuccessRegistration.as_view()),
]
