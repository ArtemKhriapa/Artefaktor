from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from apps.POI.api.serializers  import ListESSerializer
from apps.POI.models  import GisPOI, DraftGisPOI
#
# @receiver(post_save, sender=DraftGisPOI)
# def update_es_record(sender, instance, created, **kwargs):
#     GisPOI.indexing()
#     if created:
#         print('something saved')



# @receiver(post_delete, sender=GisPOI, dispatch_uid="delete_record")
# def delete_es_record(sender, instance, *args, **kwargs):
#     obj = ListESSerializer(instance)
#     obj.delete(ignore=404)
#     print('something deleted')

@receiver(post_save, sender=GisPOI)
def create_draft_poi( instance, *args, **kwargs):
    GisPOI.indexing(instance)
    print('something saved')
#
# post_save.connect(create_draft_poi, sender=DraftGisPOI)