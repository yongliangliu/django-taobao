# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-11 20:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20170308_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='recommand_id',
            field=models.CharField(default='1', max_length=4, verbose_name='\u63a8\u8350\u4ebaID'),
        ),
    ]