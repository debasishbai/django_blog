# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170315_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='caption',
            field=models.CharField(max_length=200, null=True),
        ),
    ]