# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-18 23:02
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('OTC', '0005_auto_20171218_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otc',
            name='otc',
            field=models.UUIDField(default=uuid.UUID('893fb1cc-1cf6-4b4b-bb2d-d3c64f0609aa'), editable=False),
        ),
    ]