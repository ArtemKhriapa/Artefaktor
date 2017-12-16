from django.db import models

# Create your models here.
class Registrarion(models.Model):
    registrationtext = models.CharField(max_length=200)

