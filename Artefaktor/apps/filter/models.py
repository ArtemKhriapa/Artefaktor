from django.db import models
from rest_framework import generics, status, filters
from apps.POI.models import GisPOI as GisPOI_model

# Create your models here.
class CustomFilterPOI(filters.BaseFilterBackend):
    pass