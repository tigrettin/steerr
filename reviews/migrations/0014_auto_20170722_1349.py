# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-22 11:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_auto_20170721_1149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='_100_kmph_sec',
            new_name='to_100_kmph_sec',
        ),
    ]