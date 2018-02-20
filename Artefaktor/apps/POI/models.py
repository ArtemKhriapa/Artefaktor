from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.gis.db import models as modelsgis
from taggit.managers import TaggableManager

from mptt.models import MPTTModel, TreeForeignKey
import mptt

class Category(MPTTModel):

    class Meta():
        db_table = 'category'

    # fixme: create a normal category tree  with using fixtures
    SUPPORTED_UNITS = (
        ('main','main cat'),
        ('cat1','cat1'),
        ('cat2','cat2'),
        ('1.1','sub cat1'),
        ('1.2','sub cat2'),
        ('2.1','sub_cat1'),
        ('2.2','sub_cat2')
    )

    name = models.CharField(max_length = 150,  choices= SUPPORTED_UNITS, verbose_name = 'Category')
    parent = TreeForeignKey('self', null =True, blank = True, related_name = 'CHILD', verbose_name='PARENT')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
            return "-- %s" % (self.name)

class GisPOI(modelsgis.Model):

    #FIXME: ! fields need to normal settings

    name = modelsgis.CharField(max_length=300)
    point = modelsgis.PointField(geography = True, null=True, blank=True)
    addres = modelsgis.TextField(null = True, blank=True)
    description = modelsgis.TextField()
    create_in = modelsgis.DateTimeField(auto_now_add = True)
    created_was = modelsgis.ForeignKey(User, on_delete=modelsgis.SET_NULL, null=True, blank=True)
    radius = modelsgis.PositiveIntegerField(default=0, blank = True)          # radius of POI in meters. fol localization near large  geo-objects
    image = modelsgis.ImageField(null = True, blank=True)  #:FIXME -- how it works??
    extra_data = modelsgis.TextField(null = True, blank=True)
    tags = TaggableManager()
    category = TreeForeignKey(Category,  blank=True, null=True, related_name='cat')

    def __str__(self):
        return "ID: %s" % (self.id)

mptt.register(Category,)