# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-11 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_userprofile_recommand_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='qq',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]