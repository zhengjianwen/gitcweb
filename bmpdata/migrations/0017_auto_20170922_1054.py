# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-22 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmpdata', '0016_auto_20170922_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetissue',
            name='remark',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='meetissue',
            name='suggest',
            field=models.TextField(blank=True, null=True, verbose_name='意见建议'),
        ),
    ]
