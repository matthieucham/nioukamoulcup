# Generated by Django 2.0.6 on 2019-03-08 16:07

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20190207_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Palmares',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league_instance_name', models.CharField(max_length=100)),
                ('league_instance_slogan', models.CharField(max_length=255, null=True)),
                ('league_instance_end', models.DateTimeField()),
                ('final_ranking', django.contrib.postgres.fields.jsonb.JSONField()),
                ('signings_history', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='TeamPalmaresRanking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase_name', models.CharField(max_length=100)),
                ('phase_type', models.CharField(max_length=10)),
                ('rank', models.PositiveIntegerField()),
                ('palmares', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Palmares')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Team')),
            ],
        ),
        migrations.AlterField(
            model_name='leagueinstance',
            name='slogan',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='palmares',
            field=models.ManyToManyField(through='game.TeamPalmaresRanking', to='game.Palmares'),
        ),
    ]
