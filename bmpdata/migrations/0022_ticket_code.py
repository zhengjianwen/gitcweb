# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-23 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmpdata', '0021_auto_20170923_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='code',
            field=models.CharField(max_length=64, null=True, verbose_name='编码规则'),
        ),
    ]
