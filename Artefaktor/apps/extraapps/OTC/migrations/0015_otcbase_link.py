# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-19 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OTC', '0014_auto_20171219_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='otcbase',
            name='link',
            field=models.CharField(blank=True, max_length=256, verbose_name='link'),
        ),
    ]