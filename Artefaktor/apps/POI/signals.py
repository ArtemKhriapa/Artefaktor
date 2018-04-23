from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from apps.POI.api.serializers  import ListESSerializer
from apps.POI.models  import GisPOI, DraftGisPOI


@receiver(post_save, sender=GisPOI)
def create_draft_poi( instance, *args, **kwargs):
    GisPOI.indexing(instance)