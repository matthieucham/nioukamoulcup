# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-18 22:00
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20170718_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signing',
            name='attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(default="{'score_factor': 1.0}"),
        ),
    ]