# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 17:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0005_auto_20180102_1233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrationtry',
            old_name='user_id',
            new_name='user',
        ),
    ]