# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-18 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OTC', '0008_auto_20171218_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otc',
            name='otc',
        ),
        migrations.AddField(
            model_name='otc',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
