from django.shortcuts import render
from django.core.signals import request_finished
from django.dispatch import receiver
from apps.userauth import User
import django.db.models.signals
import django.template.loader

# Create your views here.

@receiver(post_save,sender=User )
def mail_notification(sender, **kwargs):
    get_template('Artefaktor/Templates/OTC_Check_Template.html')
    send_mail(
        'Please verify your account',
        message=render_to_string('Artefaktor/Templates/OTC_Check_Template.html', {'foo': 'bar'}),
        to=User.user_email)
