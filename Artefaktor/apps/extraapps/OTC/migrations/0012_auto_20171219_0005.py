# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-19 00:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OTC', '0011_auto_20171218_2318'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OTC',
            new_name='OTCBase',
        ),
    ]