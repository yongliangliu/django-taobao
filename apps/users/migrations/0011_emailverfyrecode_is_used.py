# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-12 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20170311_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverfyrecode',
            name='is_used',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u4f7f\u7528'),
        ),
    ]
