from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class POI(models.Model):

    lon = models.FloatField()
    lat = models.FloatField()
    description = models.TextField(null=True, blank=True)
    create_in = models.DateTimeField(auto_now_add= True)
    created_was = models.ForeignKey(User, null=True, blank=True)

