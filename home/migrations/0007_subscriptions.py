# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-31 14:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0024_auto_20170727_1608'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0006_auto_20170831_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cars', models.ManyToManyField(related_name='followers', to='reviews.Car')),
                ('members', models.ManyToManyField(related_name='followers', to='home.Subscriptions')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
