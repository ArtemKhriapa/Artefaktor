from django.db import models
from django.db.models.signals import post_save

# Create your models here.
class MailerLogModel(models.Model):
    mail_sent = models.DateTimeField(auto_now_add=True)
