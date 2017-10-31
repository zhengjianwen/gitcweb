# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-18 12:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bmpdata', '0003_auto_20170915_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileCollect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Meetissue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('company', models.CharField(max_length=128, verbose_name='公司')),
                ('position', models.CharField(max_length=64, verbose_name='职位')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('email', models.EmailField(max_length=256, verbose_name='邮箱')),
                ('addr', models.CharField(max_length=256, verbose_name='地址')),
                ('photo', models.CharField(max_length=256, verbose_name='照片')),
                ('summary', models.CharField(max_length=256, verbose_name='简介')),
                ('speech_experience', models.TextField(verbose_name='简介')),
                ('interest', models.CharField(max_length=256, verbose_name='兴趣专场')),
                ('remark', models.CharField(max_length=256, verbose_name='备注')),
                ('theme', models.CharField(max_length=256, verbose_name='演讲主题')),
                ('content', models.TextField(verbose_name='演讲内容')),
                ('innovate', models.SmallIntegerField(verbose_name='主题创新')),
                ('hot_topic', models.SmallIntegerField(verbose_name='主题创新')),
                ('experience', models.SmallIntegerField(verbose_name='实战经验')),
                ('generality', models.SmallIntegerField(verbose_name='通用性')),
                ('suggest', models.TextField(verbose_name='意见建议')),
            ],
        ),
        migrations.CreateModel(
            name='Memberinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='姓名')),
                ('sex', models.CharField(blank=True, max_length=8, null=True, verbose_name='性别')),
                ('age', models.SmallIntegerField(blank=True, null=True, verbose_name='年龄')),
            ],
        ),
        migrations.CreateModel(
            name='MemberPCollect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmpdata.Personnel', verbose_name='嘉宾')),
                ('mpc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmpdata.Memberinfo', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('company', models.CharField(max_length=128, verbose_name='公司')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('position', models.CharField(max_length=64, verbose_name='职位')),
                ('email', models.EmailField(max_length=256, verbose_name='邮箱')),
                ('intention', models.TextField(verbose_name='赞助意向')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=11, verbose_name='票务名称')),
            ],
        ),
        migrations.AddField(
            model_name='filecollect',
            name='mf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmpdata.Memberinfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='filecollect',
            name='mp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bmpdata.Files', verbose_name='文档'),
        ),
    ]
