# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import document.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('filename', models.FileField(upload_to=document.models.generate_filename)),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
