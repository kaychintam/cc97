# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-05 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0002_auto_20170305_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='icon',
            field=models.CharField(default='default.jpeg', max_length=255),
        ),
    ]
