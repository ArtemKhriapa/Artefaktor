from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class OTCBase(models.Model):
    '''base OTC model'''
    otc = models.UUIDField(verbose_name="UUID code", default=uuid.uuid4)
    created_in = models.DateTimeField(verbose_name="created in", auto_now_add=True)
    used_in = models.DateTimeField(verbose_name="used in", null = True, blank = True)
    is_used = models.BooleanField(verbose_name="is used", default = False)

    def apply(self):
        self.is_used = True         #utilization
        self.used_in = timezone.now()
        self.save()

    def __str__(self):
        return "ID: %s, Time: %s, OTC: %s, Used: %s" % \
               (self.id, self.created_in, self.otc, self.is_used)


class OTCRegistration(OTCBase):
    '''user registration OTC model'''
    user = models.ForeignKey(User, related_name = 'reg_otc', null=True, blank=True)
    link = models.CharField(max_length=256, verbose_name="link", blank=True)

    def linkgenerate(self):
        link = 'http://127.0.0.1:8000/api/registration/' + str(self.otc)
        return link

    def save(self, *args, **kwargs):
        self.link = self.linkgenerate() # only for add in DB. delete it next time
        super().save(*args, **kwargs)
