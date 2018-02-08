#from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.gis.db import models as modelsgis
from taggit.managers import TaggableManager

class GisPOI(modelsgis.Model):

    #FIXME: ! fields need to normal settings

    name = modelsgis.CharField(max_length=300)
    point = modelsgis.PointField(geography = True, null=True, blank=True)
    addres = modelsgis.TextField(null = True, blank=True)
    description = modelsgis.TextField()
    create_in = modelsgis.DateTimeField(auto_now_add = True)
    created_was = modelsgis.ForeignKey(User, on_delete=modelsgis.SET_NULL, null=True, blank=True)
    radius = modelsgis.IntegerField(default=0, blank = True)          # radius of POI in meters. fol localization near large  geo-objects
    image = modelsgis.ImageField(null = True, blank=True)  #:FIXME -- how it works??
    extra_data = modelsgis.TextField(null = True, blank=True)
    tags = TaggableManager()


    def __str__(self):
        return "ID: %s" % (self.id)