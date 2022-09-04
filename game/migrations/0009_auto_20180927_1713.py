# Generated by Django 2.0.6 on 2018-09-27 15:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_league_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]