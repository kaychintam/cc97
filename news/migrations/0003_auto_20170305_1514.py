# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-05 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20170305_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('readerName', models.CharField(max_length=255)),
                ('newsId', models.IntegerField()),
                ('commentNo', models.IntegerField()),
                ('content', models.CharField(max_length=255)),
                ('commentDate', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='commentNo',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
