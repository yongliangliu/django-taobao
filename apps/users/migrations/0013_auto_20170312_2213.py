# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-12 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_userprofile_alipay_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nick_name',
            field=models.CharField(default='', max_length=50, verbose_name='\u59d3\u540d'),
        ),
    ]
