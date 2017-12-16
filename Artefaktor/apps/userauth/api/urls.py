from django.conf.urls import url
from apps.userauth.api import views

urlpatterns = [
    url(r'^$', views.RegistrationViev()),
]