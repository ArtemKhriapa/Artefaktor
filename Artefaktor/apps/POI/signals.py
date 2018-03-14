from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from apps.POI.api.serializers  import ListESSerializer
from apps.POI.models  import GisPOI

@receiver(pre_save, sender=GisPOI, dispatch_uid="update_record")
def update_es_record(sender, instance, **kwargs):
    obj = ListESSerializer(instance)
    obj.save()
    print('something saved')

@receiver(post_delete, sender=GisPOI, dispatch_uid="delete_record")
def delete_es_record(sender, instance, *args, **kwargs):
    obj = ListESSerializer(instance)
    obj.delete(ignore=404)
    print('something deleted')