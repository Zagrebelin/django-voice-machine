# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voice', '0006_auto_20170605_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weather',
            name='temperature',
            field=models.IntegerField(),
        ),
    ]
