# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-13 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20170312_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to='image/%Y/%m'),
        ),
    ]
