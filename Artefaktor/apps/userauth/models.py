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

    otc = models.ForeignKey(OTCRegistration, related_name='o_t_c')
    registrationtext = models.CharField(max_length=200, default="in this plase will be registration form")
    created_in = models.DateTimeField(auto_now_add= True)
    is_finished = models.BooleanField(default=False)
    finished_in = models.DateTimeField(null = True, blank = True)

    def try_register(self):
        # in this place send link (OTC.link) to self.user_email
        pass

    def finishing(self):
        self.is_finished = True
        self.finished_in = timezone.now()
        #
        # in this place send email "вы член!"
        self.save()