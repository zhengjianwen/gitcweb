# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-25 08:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmpdata', '0024_auto_20170925_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='referee',
            field=models.CharField(max_length=32, null=True, verbose_name='推荐人'),
        ),
    ]