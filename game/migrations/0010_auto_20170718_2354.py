# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-18 21:54
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20170718_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signing',
            name='attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'factor': 1.0}),
        ),
        migrations.AlterUniqueTogether(
            name='leagueinstancephase',
            unique_together=set([]),
        ),
    ]