# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import pdf.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.FileField(upload_to=pdf.models.generate_filename)),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bid.Bid')),
            ],
        ),
    ]
