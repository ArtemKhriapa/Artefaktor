# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-01 13:43
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GisPOI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326)),
                ('create_in', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
