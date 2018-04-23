from django.core.mail import send_mail
from apps.userauth.models import RegistrationTry
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import get_template, render_to_string


@receiver(post_save, sender=RegistrationTry)
def mail_notification(*args,**kwargs):
    rendered = get_template('Templates/OTC_Check_Template.html')
    html_msg = render_to_string('Templates/OTC_Check_Template.html', {'foo': 'bar'})
    send_mail(
        'Please verify your account',
        message= rendered,
        from_email= "no_reply_art@outlook.com" ,
        recipient_list=["self.user_email"],
        html_message= html_msg)
