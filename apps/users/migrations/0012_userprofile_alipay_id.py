# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-12 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_emailverfyrecode_is_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='alipay_id',
            field=models.CharField(default='', max_length=30, verbose_name='\u652f\u4ed8\u5b9d\u8d26\u53f7'),
        ),
    ]
