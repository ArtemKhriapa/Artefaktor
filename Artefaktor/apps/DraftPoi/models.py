from django.db import models
from django.contrib.gis.db import models as models
from apps.POI.models import GisPOI
# Create your models here.
class DraftPoi(GisPOI):
    submitted_by = models.ForeignKey('userauth.RegistrationTry',
                                     on_delete=models.CASCADE,)
    moderated_on = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(False)
    declined_reason = models.TextField(null = True, blank=True)






