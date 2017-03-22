# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 19:12
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
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=2000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bid.Bid')),
            ],
        ),
    ]
