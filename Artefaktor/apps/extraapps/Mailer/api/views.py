from django.shortcuts import render
from django.core.signals import request_finished
from django.dispatch import receiver
from apps.userauth import User

# Create your views here.

@receiver(registration_mail,sender=User )
def mail_sender(sender, **kwargs):
    send_mail(
        'Please verify your account',
        message=render_to_string('OTC_Check_Templates.html', {'foo': 'bar'}),
        to=User.user_email)