# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-19 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prendas', '0003_auto_20180619_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garmentstocheck',
            name='refusedText',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
