# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-26 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POI', '0007_auto_20180226_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
