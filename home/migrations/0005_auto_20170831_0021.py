# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-30 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0024_auto_20170727_1608'),
        ('home', '0004_auto_20170830_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='members',
            field=models.ManyToManyField(related_name='followers', to='home.Subscriptions'),
        ),
        migrations.RemoveField(
            model_name='subscriptions',
            name='cars',
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='cars',
            field=models.ManyToManyField(related_name='followers', to='reviews.Car'),
        ),
    ]