from django.db import models
from django.utils import timezone
from apps.extraapps.OTC.models import OTCRegistration

# Create your models here.

class RegistrationForm(models.Model):
    '''rough registration form. fix next time'''
    user_nickname = models.CharField(max_length=100, blank=True, null=True, default = None)
    user_firstname = models.CharField(max_length=100, blank=True, null=True, default = None)
    user_lastname = models.CharField(max_length=100, blank=True, null=True, default = None)
    user_email = models.EmailField(max_length=200, blank=True, null=True, default = None)

class RegistrarionTry(RegistrationForm):

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
        pass

    def finishing(self):
        self.is_finished = True
        self.finished_in = timezone.now()
        # in this place create new user (using inf from this model)
        # in this place send email "now you a "член!!!" "
        self.save()