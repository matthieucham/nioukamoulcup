# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-08 20:55
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20170706_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='bank_account', serialize=False, to='game.Team')),
                ('balance', models.DecimalField(decimal_places=1, max_digits=4)),
                ('adjust', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccountHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=1, max_digits=4)),
                ('new_balance', models.DecimalField(decimal_places=1, max_digits=4)),
                ('info', django.contrib.postgres.fields.jsonb.JSONField()),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.BankAccount')),
            ],
        ),
    ]