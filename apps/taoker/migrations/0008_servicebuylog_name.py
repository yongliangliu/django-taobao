# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-11 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taoker', '0007_serviceuselog'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicebuylog',
            name='name',
            field=models.CharField(default='', max_length=50, verbose_name='\u8d2d\u4e70\u670d\u52a1\u540d\u79f0'),
        ),
    ]
