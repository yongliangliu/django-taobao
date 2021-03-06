# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-11 16:55
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taoker', '0005_auto_20170311_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u670d\u52a1\u540d\u79f0')),
                ('desc', models.CharField(max_length=300, verbose_name='\u670d\u52a1\u63cf\u8ff0')),
                ('price', models.IntegerField(default=100, verbose_name='\u4ef7\u683c')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u6dd8\u5ba2\u670d\u52a1\u5546\u54c1',
                'verbose_name_plural': '\u6dd8\u5ba2\u670d\u52a1\u5546\u54c1',
            },
        ),
        migrations.CreateModel(
            name='ServiceBuyLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mount', models.IntegerField(default=10, verbose_name='\u8d2d\u4e70\u6570\u91cf')),
                ('rate', models.DecimalField(decimal_places=2, default=0.97, max_digits=7, verbose_name='\u8d2d\u4e70\u6298\u6263')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='\u8ba2\u5355\u603b\u4ef7')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taoker.Service', verbose_name='\u8d2d\u4e70\u7684\u670d\u52a1')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u6dd8\u5ba2\u670d\u52a1\u8d2d\u4e70\u8bb0\u5f55',
                'verbose_name_plural': '\u6dd8\u5ba2\u670d\u52a1\u8d2d\u4e70\u8bb0\u5f55',
            },
        ),
    ]
