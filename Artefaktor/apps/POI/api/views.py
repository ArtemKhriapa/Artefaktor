from django.http import Http404
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from apps.POI.api.serializers  import  GisPOISerializer, NewGisPOISerializer
from apps.POI.models import GisPOI as GisPOI_model



class NewGisPOI(generics.CreateAPIView):
    serializer_class = NewGisPOISerializer
    model = GisPOI_model

    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        res.status_code == status.HTTP_201_CREATED
        return res

class GisPOI(generics.RetrieveAPIView):
    queryset = GisPOI_model.objects.all()
    serializer_class = GisPOISerializer

    def get_object(self):
        return get_object_or_404(GisPOI_model, id=self.kwargs.get('POI_id'))