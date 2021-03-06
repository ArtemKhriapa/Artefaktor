# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-20 15:37
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=25, null=True, unique=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Category', to='POI.Category')),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='DraftGisPOI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326)),
                ('addres', models.TextField(blank=True, null=True)),
                ('description', models.TextField()),
                ('create_in', models.DateTimeField(auto_now_add=True)),
                ('radius', models.PositiveIntegerField(blank=True, default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('extra_data', models.TextField(blank=True, null=True)),
                ('is_moderate', models.BooleanField(default=False)),
                ('category', models.ManyToManyField(blank=True, related_name='cat', to='POI.Category')),
                ('created_was', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GisPOI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326)),
                ('addres', models.TextField(blank=True, null=True)),
                ('description', models.TextField()),
                ('create_in', models.DateTimeField(auto_now_add=True)),
                ('radius', models.PositiveIntegerField(blank=True, default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('extra_data', models.TextField(blank=True, null=True)),
                ('is_moderate', models.BooleanField(default=False)),
                ('moderation_on', models.DateField(auto_now_add=True, null=True)),
                ('moderated_was', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
