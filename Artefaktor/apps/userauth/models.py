from django.db import models

# Create your models here.
class Registrarion(models.Model):
    registration_text = models.CharField(max_length=200)

