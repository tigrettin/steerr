# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-18 12:54
from __future__ import unicode_literals

from django.db import migrations, models
import reviews.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0026_auto_20171116_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/reviews/images/cars/', validators=[reviews.models.file_size]),
        ),
    ]