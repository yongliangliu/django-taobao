# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-08 15:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20170307_1956'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='birday',
            new_name='birth_day',
        ),
    ]
