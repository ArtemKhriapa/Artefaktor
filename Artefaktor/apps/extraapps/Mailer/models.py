from django.db import models
django.db.models.signals.post_save

# Create your models here.
class MailerLogModel(models.Model):
    mail_sent = models.DateTimeField(auto_now_add=True)
