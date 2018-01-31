from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.gis.db import models as modelsgis

class POI(models.Model):

    lon = models.FloatField()
    lat = models.FloatField()
    description = models.TextField(null=True, blank=True)
    create_in = models.DateTimeField(auto_now_add= True)
    created_was = models.ForeignKey(User, null=True, blank=True)

class GisPOI(modelsgis.Model): #experiment withs GIS

    geometry = modelsgis.GeometryField(null = True, blank=True)
    point = modelsgis.PointField(null=True, blank=True)
    polygon = modelsgis.PolygonField(null=True, blank=True)

    def __str__(self):
        return "ID: %s" % (self.id)