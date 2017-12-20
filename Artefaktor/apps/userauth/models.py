from django.db import models
from django.utils import timezone
from apps.extraapps.OTC.models import OTCRegistration


class RegistrarionTry(models.Model):

    user_nickname = models.CharField(max_length=100, blank=True, null=True)
    user_firstname = models.CharField(max_length=100, blank=True, null=True)
    user_lastname = models.CharField(max_length=100, blank=True, null=True)
    user_email = models.EmailField(max_length=200, blank=True, null=True)
    extra_data = models.TextField(blank=True, null=True)
    otc = models.ForeignKey(OTCRegistration, related_name='reg_otc', null=True)
    created_in = models.DateTimeField(auto_now_add= True)
    is_finished = models.BooleanField(default=False)
    finished_in = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return "ID: %s, Created: %s, E-mail: %s" % \
               (self.id, self.created_in, self.user_email)

    def try_register(self):
        # somewhere here create OTC
        # in this place send link (OTC.link) to self.user_email
        self.save()

    def finishing(self):
        self.is_finished = True
        self.finished_in = timezone.now()
        # in this place create new user (using inf from this model)
        # in this place send email "now you a "член!!!" "
        self.save()
