# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(blank=True, help_text='Enter Payment Description', max_length=100)),
                ('amount', models.FloatField(blank=True, help_text='Enter Payment Amount', max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
