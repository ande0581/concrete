# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0004_auto_20170205_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='custom_down_payment',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
