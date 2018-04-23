from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.gis.db import models as modelsgis
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
import mptt
from apps.POI.esearch import GisPOIIndex


class Category(MPTTModel):
    class Meta:
        db_table = 'category'

    name = models.CharField(max_length=150)
    slug = modelsgis.SlugField(null=True, unique=True, max_length=25)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='Category')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return "-- %s" % (self.name)


mptt.register(Category, )


class BaseGisPOI(modelsgis.Model):
    name = modelsgis.CharField(max_length=300)
    point = modelsgis.PointField(geography=True, null=True, blank=True)
    addres = modelsgis.TextField(null=True, blank=True)
    description = modelsgis.TextField()
    create_in = modelsgis.DateTimeField(auto_now_add=True)
    radius = modelsgis.PositiveIntegerField(default=0, blank=True)
    image = modelsgis.ImageField(null=True, blank=True)
    extra_data = modelsgis.TextField(null=True, blank=True)
    tags = TaggableManager()
    is_moderate = models.BooleanField(default=False)

    class Meta:
        abstract = True


class DraftGisPOI(BaseGisPOI):
    category = modelsgis.ManyToManyField(Category, blank=True, related_name='draftpoi')
    created_was = modelsgis.ForeignKey(User, on_delete=modelsgis.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "ID: %s" % (self.id)


class GisPOI(BaseGisPOI):
    created_was = modelsgis.ForeignKey(User, on_delete=modelsgis.SET_NULL, null=True, blank=True,
                                       related_name='cratedpoi')
    category = modelsgis.ManyToManyField(Category, blank=True, related_name='poi')
    moderated_was = modelsgis.ForeignKey(User, on_delete=modelsgis.SET_NULL, null=True, blank=True)
    moderation_on = models.DateField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return "ID: %s" % (self.id)

    @property
    def anchor(self):
        return {"geolocation": { "lat": self.point.coords[1], "lon": self.point.coords[0] }}

    @property
    def text(self):
        return {
         "title": self.name,
         "description": self.description,
        }

    def indexing(self):
        # print('indexing')
        obj = GisPOIIndex(
            meta={'id': self.id},
            id=self.id,
            name=self.name,
            description=self.description,
            date=self.create_in
        )
        # print('indexing POI : ', obj.name, obj.description)
        obj.save()
        return obj.to_dict(include_meta=True)
