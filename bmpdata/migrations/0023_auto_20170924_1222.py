# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-24 04:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bmpdata', '0022_ticket_code'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='filecollect',
            unique_together=set([('mf', 'mp')]),
        ),
        migrations.AlterUniqueTogether(
            name='memberpcollect',
            unique_together=set([('mpc', 'mp')]),
        ),
    ]
