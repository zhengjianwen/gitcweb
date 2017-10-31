# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-19 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmpdata', '0004_auto_20170918_2005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filecollect',
            options={'verbose_name': '文档收藏'},
        ),
        migrations.AlterModelOptions(
            name='meetissue',
            options={'verbose_name': '议题提交'},
        ),
        migrations.AlterModelOptions(
            name='memberinfo',
            options={'verbose_name': '会员管理'},
        ),
        migrations.AlterModelOptions(
            name='memberpcollect',
            options={'verbose_name': '会员收藏'},
        ),
        migrations.AlterModelOptions(
            name='sponsor',
            options={'verbose_name': '赞助意向'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': '票务管理'},
        ),
        migrations.AddField(
            model_name='article',
            name='weight',
            field=models.SmallIntegerField(default=1, verbose_name='权重'),
        ),
        migrations.AddField(
            model_name='contact',
            name='weight',
            field=models.SmallIntegerField(default=1, verbose_name='权重'),
        ),
        migrations.AddField(
            model_name='files',
            name='weight',
            field=models.SmallIntegerField(default=1, verbose_name='权重'),
        ),
        migrations.AddField(
            model_name='html',
            name='weight',
            field=models.SmallIntegerField(default=1, verbose_name='权重'),
        ),
        migrations.AddField(
            model_name='imgs',
            name='weight',
            field=models.SmallIntegerField(default=1, verbose_name='权重'),
        ),
        migrations.AddField(
            model_name='meetissue',
            name='ctime',
            field=models.TimeField(auto_now=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='memberinfo',
            name='ctime',
            field=models.TimeField(auto_now=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='memberinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='weight',
            field=models.SmallIntegerField(default=1, verbose_name='权重'),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='ctime',
            field=models.TimeField(auto_now=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='weight',
            field=models.SmallIntegerField(default=1, verbose_name='权重'),
        ),
        migrations.AddField(
            model_name='video',
            name='weight',
            field=models.SmallIntegerField(default=1, verbose_name='权重'),
        ),
        migrations.AlterField(
            model_name='meetissue',
            name='hot_topic',
            field=models.SmallIntegerField(verbose_name='话题热度'),
        ),
        migrations.AlterField(
            model_name='meetissue',
            name='speech_experience',
            field=models.TextField(verbose_name='演讲经验'),
        ),
        migrations.AlterField(
            model_name='memberinfo',
            name='phone',
            field=models.CharField(max_length=11, unique=True, verbose_name='手机号'),
        ),
    ]