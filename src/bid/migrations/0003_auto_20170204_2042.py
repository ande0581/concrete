# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bid', '0002_auto_20170204_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='billto_city_st_zip',
            field=models.CharField(blank=True, max_length=100, verbose_name='Alternative Bill To City, ST, ZIP'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='billto_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Alternative Bill To Name'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='billto_street',
            field=models.CharField(blank=True, max_length=100, verbose_name='Alternative Bill To Street'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='billto_telephone',
            field=models.CharField(blank=True, max_length=10, verbose_name='Alternative Bill To Telephone Number'),
        ),
    ]