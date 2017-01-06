# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2000)),
                ('quantity', models.FloatField()),
                ('cost', models.FloatField()),
                ('total', models.FloatField()),
                ('bid_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bid.Bid')),
            ],
        ),
    ]
