# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-09 17:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OraginData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u539f\u59cb\u6807\u9898')),
                ('add_price', models.IntegerField(default=0, verbose_name='\u52a0\u4ef7')),
                ('url', models.CharField(default='', max_length=200, verbose_name='\u4e0a\u5bb6\u5730\u5740')),
                ('good_code', models.CharField(max_length=100, verbose_name='\u5546\u5bb6\u7f16\u7801')),
                ('download', models.FileField(upload_to='taoke_data/oragin/%Y/%m', verbose_name='\u539f\u59cb\u6570\u636e\u5305')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('category', models.CharField(default='', max_length=20, verbose_name='\u6570\u636e\u5305\u7c7b\u522b')),
                ('tag', models.CharField(default='', max_length=10, verbose_name='\u6570\u636e\u6807\u7b7e')),
            ],
            options={
                'verbose_name': '\u539f\u59cb\u6570\u636e\u5305',
                'verbose_name_plural': '\u539f\u59cb\u6570\u636e\u5305',
            },
        ),
    ]
