# Generated by Django 2.1.9 on 2021-09-03 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ligue1', '0004_auto_20181008_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='joueur',
            name='indraftable',
            field=models.NullBooleanField(),
        ),
    ]