from django.shortcuts import render
from rest_framework import generics
from apps.DraftPoi.api.serializers import DraftPoiSerializer
from apps.DraftPoi.models import DraftPoi


class NewDraftPoi(generics.CreateAPIView):
    serializer_class = DraftPoiSerializer
    model = DraftPoi

    def post(self, *args, **kwargs):
        res = super().post(*args, **kwargs)
        return res

class DeleteDraftPoi(generics.RetrieveDestroyAPIView):
    serializer_class = DraftPoiSerializer
    model = DraftPoi

    def delete(self, request, *args, **kwargs):
        res = super(DeleteDraftPoi, self).delete(*args, **kwargs)
        return res