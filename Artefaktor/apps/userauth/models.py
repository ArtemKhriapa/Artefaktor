from django.db import models
from django.utils import timezone
from apps.extraapps.OTC.models import OTCRegistration
from django.contrib.auth.models import User



class RegistrationTry(models.Model):

    user_id = models.ForeignKey(User, related_name='registration',null=True, blank = True)
    user_nickname = models.CharField(max_length=100, blank=True, null=True)
    user_firstname = models.CharField(max_length=100, blank=True, null=True)
    user_lastname = models.CharField(max_length=100, blank=True, null=True)
    user_email = models.EmailField(max_length=200, blank=True, null=True)
    extra_data = models.TextField(blank=True, null=True)
    otc = models.ForeignKey(OTCRegistration, related_name='reg_otc', null=True, blank = True)
    created_in = models.DateTimeField(auto_now_add= True)
    is_finished = models.BooleanField(default=False)
    finished_in = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return "ID: %s, Created: %s, E-mail: %s" % \
               (self.id, self.created_in, self.user_email)

    def finish(self):
        self.is_finished = True
        self.finished_in = timezone.now()

        new_user = User.objects.create_user(
            str(self.user_nickname),
            email = self.user_email,
            password = 'password'    # create request password next time
        )

        # in this place send email "now you a "dick!!!"
        print('reg ok')

        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            new_otc = OTCRegistration.objects.create()
            self.otc = new_otc
            
            # somewhere in this place send link (OTC.link) to self.user_email
        return super().save(*args, **kwargs)
