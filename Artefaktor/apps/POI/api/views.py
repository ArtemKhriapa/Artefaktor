from django.http import Http404
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from apps.POI.api.serializers  import POISerializer, GisPOISerializer
from apps.POI.models import POI as POI_model
from apps.POI.models import GisPOI as GisPOI_model
from django import forms
from django.core.mail import send_mail


class POI(generics.CreateAPIView, generics.RetrieveAPIView): #next time remoove CreateAPIView
    queryset = POI_model.objects.all()
    serializer_class = POISerializer

    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        if res.status_code == status.HTTP_201_CREATED:
            pass
        return res

    def get_object(self):
        try:
            poi = get_object_or_404(POI_model, id=self.kwargs.get('POI_id'))
            return poi
        except Exception as e:
            print(e)
            raise Http404


class NewGisPOI(generics.CreateAPIView):        #exp
    serializer_class = GisPOISerializer
    model = GisPOI_model


class GisPOI(generics.RetrieveAPIView):
    queryset = GisPOI_model.objects.all()
    serializer_class = GisPOISerializer

    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        if res.status_code == status.HTTP_201_CREATED:
            pass
        return res

    def get_object(self):
        try:
            poi = get_object_or_404(GisPOI_model, id=self.kwargs.get('GIS_POI_id'))
            return poi
        except Exception as e:
            print(e)
            raise Http404