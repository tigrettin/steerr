# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-26 14:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0019_auto_20170726_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created']},
        ),
    ]
