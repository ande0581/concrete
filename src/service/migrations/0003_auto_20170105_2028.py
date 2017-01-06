# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_service_protected'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('concrete', 'concrete'), ('rebar', 'rebar'), ('stamp', 'stamp')], default='No Category', max_length=2000),
        ),
    ]
