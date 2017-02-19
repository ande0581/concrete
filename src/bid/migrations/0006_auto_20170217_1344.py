# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0005_auto_20170205_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='custom_down_payment',
            field=models.FloatField(blank=True, null=True, verbose_name='Custom Down Payment: Blank means default down payment. Enter -1 for no down payment or any other value for custom down payment'),
        ),
    ]
