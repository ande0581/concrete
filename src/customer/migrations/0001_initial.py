# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text="Enter the customer's first name", max_length=64)),
                ('last_name', models.CharField(blank=True, help_text="Enter the customer's last name", max_length=64)),
                ('company_name', models.CharField(blank=True, help_text='Enter the company name', max_length=128)),
                ('email', models.EmailField(blank=True, help_text='Enter the customer email address', max_length=254)),
                ('telephone', models.CharField(blank=True, help_text='Enter the customer telephone number', max_length=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Customers',
            },
        ),
    ]
