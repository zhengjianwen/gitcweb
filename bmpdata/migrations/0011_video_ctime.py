# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-20 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmpdata', '0010_imgs_ctime'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='ctime',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='创建时间'),
        ),
    ]
