# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 07:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_caption'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image_name',
        ),
    ]
