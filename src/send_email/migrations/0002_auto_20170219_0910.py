# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 15:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('send_email', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emaillog',
            options={'ordering': ['-timestamp']},
        ),
    ]
