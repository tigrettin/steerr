# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-20 10:29
from __future__ import unicode_literals

from django.db import migrations, models
import marketplace.models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0012_auto_20171120_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='photo',
        ),
        migrations.AddField(
            model_name='listing',
            name='photo1',
            field=models.ImageField(blank=True, null=True, upload_to='static/marketplace/images/', validators=[marketplace.models.file_size]),
        ),
        migrations.AddField(
            model_name='listing',
            name='photo2',
            field=models.ImageField(blank=True, null=True, upload_to='static/marketplace/images/', validators=[marketplace.models.file_size]),
        ),
        migrations.AddField(
            model_name='listing',
            name='photo3',
            field=models.ImageField(blank=True, null=True, upload_to='static/marketplace/images/', validators=[marketplace.models.file_size]),
        ),
        migrations.AddField(
            model_name='listing',
            name='photo4',
            field=models.ImageField(blank=True, null=True, upload_to='static/marketplace/images/', validators=[marketplace.models.file_size]),
        ),
        migrations.AddField(
            model_name='listing',
            name='photo5',
            field=models.ImageField(blank=True, null=True, upload_to='static/marketplace/images/', validators=[marketplace.models.file_size]),
        ),
    ]
