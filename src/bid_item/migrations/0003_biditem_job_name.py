# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-29 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid_item', '0002_auto_20170109_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='biditem',
            name='job_name',
            field=models.CharField(default='Driveway', max_length=100),
            preserve_default=False,
        ),
    ]