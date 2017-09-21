# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-28 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_auto_20170728_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='color',
            field=models.CharField(choices=[('WE', 'White'), ('BK', 'Black'), ('SR', 'Silver'), ('GY', 'Grey'), ('RD', 'Red'), ('BE', 'Blue'), ('GN', 'Green'), ('YW', 'Yellow'), ('OE', 'Orange')], max_length=2),
        ),
        migrations.AlterField(
            model_name='listing',
            name='condition',
            field=models.CharField(choices=[('N', 'New'), ('U', 'Used')], max_length=1),
        ),
    ]
