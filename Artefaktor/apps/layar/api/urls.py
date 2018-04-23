from django.conf.urls import url
from apps.layar.api.views import LayarView

urlpatterns = [
    url(r'^$', LayarView.as_view()),
    ]