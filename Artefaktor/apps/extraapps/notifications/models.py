from django.db import models
from django.core.mail import send_mail


def AutoMailer():
    send_mail(
        'One time Key',
        'Here is the message.',# Here should be one time code
        'from@example.com',# our mail
        ['to@example.com'],# FK to Mail identified by user
        fail_silently=False,
    )
