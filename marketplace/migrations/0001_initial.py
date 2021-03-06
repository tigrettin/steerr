# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-28 15:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0024_auto_20170727_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('mileage', models.IntegerField()),
                ('year', models.IntegerField()),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('color', models.CharField(max_length=10)),
                ('condition', models.CharField(max_length=10)),
                ('seller', models.CharField(max_length=50)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
