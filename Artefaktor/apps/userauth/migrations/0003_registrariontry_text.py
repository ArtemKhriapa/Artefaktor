# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-19 02:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0002_auto_20171219_0215'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrariontry',
            name='text',
            field=models.CharField(default='some text', max_length=50),
        ),
    ]