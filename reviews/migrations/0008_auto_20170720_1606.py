# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-20 14:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20170720_1533'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ('make',)},
        ),
    ]
