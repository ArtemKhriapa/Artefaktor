from django.shortcuts import get_object_or_404
from rest_framework import generics
from apps.userauth.api.serializers import SomeSerializer


class SomeView(generics.ListCreateAPIView):
    pass