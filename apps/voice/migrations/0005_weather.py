# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-12 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voice', '0004_auto_20170503_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(unique=True)),
                ('wind', models.CharField(max_length=200)),
                ('temperature', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
    ]