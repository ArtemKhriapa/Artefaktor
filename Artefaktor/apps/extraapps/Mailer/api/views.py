from django.core.mail import send_mail
from Artefaktor.Artefaktor.apps.userauth.models import RegistrationTry
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import get_template, render_to_string
from django.contrib.auth import User

@receiver(post_save,sender=RegistrationTry)
def mail_notification(sender, **kwargs):
    get_template('Artefaktor/Templates/OTC_Check_Template.html')
    send_mail(
        'Please verify your account',
        message=render_to_string('Artefaktor/Templates/OTC_Check_Template.html', {'foo': 'bar'}),
        from_email= no_reply_art@outlook.com,
        recipient_list=User.email)
