# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-15 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20170109_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='measurement',
            field=models.CharField(default='tobedeleted', max_length=30),
            preserve_default=False,
        ),
    ]