# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-31 14:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20170831_0021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptions',
            name='cars',
        ),
        migrations.RemoveField(
            model_name='subscriptions',
            name='members',
        ),
        migrations.RemoveField(
            model_name='subscriptions',
            name='user',
        ),
        migrations.DeleteModel(
            name='Subscriptions',
        ),
    ]
