# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-20 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('OTC', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrarionTry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_nickname', models.CharField(blank=True, max_length=100, null=True)),
                ('user_firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('user_lastname', models.CharField(blank=True, max_length=100, null=True)),
                ('user_email', models.EmailField(blank=True, max_length=200, null=True)),
                ('extra_data', models.TextField(blank=True, null=True)),
                ('created_in', models.DateTimeField(auto_now_add=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('finished_in', models.DateTimeField(blank=True, null=True)),
                ('otc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reg_otc', to='OTC.OTCRegistration')),
            ],
        ),
    ]
