# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-18 23:15
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('OTC', '0009_auto_20171218_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otc',
            name='id',
        ),
        migrations.AddField(
            model_name='otc',
            name='otc',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]