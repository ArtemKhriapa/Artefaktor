from django.db import models
from django.utils import timezone
from apps.extraapps.OTC.models import OTCRegistration
from django.contrib.auth.models import User
from apps.extraapps.Mailer.models import EmailLog


class RegistrationTry(models.Model):

    user = models.OneToOneField(User, related_name='registration',null=True, blank = True)
    username = models.CharField(max_length=100,  blank=True, null=True)
    user_firstname = models.CharField(max_length=100, blank=True, null=True)
    user_lastname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=200,  blank=True, null=True)
    extra_data = models.TextField(blank=True, null=True)
    otc = models.ForeignKey(OTCRegistration, related_name='reg_otc', null=True, blank = True)
    created_in = models.DateTimeField(auto_now_add= True)
    is_finished = models.BooleanField(default=False)
    finished_in = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return "ID: %s, Created: %s, E-mail: %s" % \
               (self.id, self.created_in, self.email)

    def finish(self):
        self.is_finished = True     #utilization
        self.finished_in = timezone.now()
        self.otc.apply()            #utilization
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            new_otc = OTCRegistration.objects.create()
            self.otc = new_otc
            reason = 'Confirmation of registration'
            mail = EmailLog.objects.create(
                mail_to=self.email,
                text =str('Follow the link' + self.otc.link + 'to confirm your registration'))
            mail.save()
            mail.sendmail(reason)
            # somewhere in this place send link (OTC.link) to self.user_email

        return super().save(*args, **kwargs)

