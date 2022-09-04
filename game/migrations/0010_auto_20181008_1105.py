# Generated by Django 2.0.6 on 2018-10-08 09:05

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ligue1', '0004_auto_20181008_1105'),
        ('game', '0009_auto_20180927_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='DraftPick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pick_order', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DraftSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('closing', models.DateTimeField()),
                ('is_solved', models.BooleanField(default=False)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('merkato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Merkato')),
            ],
        ),
        migrations.CreateModel(
            name='DraftSessionRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField()),
                ('draft_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.DraftSession')),
                ('signing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.Signing')),
            ],
        ),
        migrations.AlterField(
            model_name='leaguedivision',
            name='lower_division',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='upper', to='game.LeagueDivision'),
        ),
        migrations.AlterField(
            model_name='leaguedivision',
            name='upper_division',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lower', to='game.LeagueDivision'),
        ),
        migrations.AlterField(
            model_name='team',
            name='attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='draftsessionrank',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.Team'),
        ),
        migrations.AddField(
            model_name='draftsession',
            name='teams',
            field=models.ManyToManyField(through='game.DraftSessionRank', to='game.Team'),
        ),
        migrations.AddField(
            model_name='draftpick',
            name='draft_session_rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='picks', to='game.DraftSessionRank'),
        ),
        migrations.AddField(
            model_name='draftpick',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ligue1.Joueur'),
        ),
        migrations.AlterUniqueTogether(
            name='draftsessionrank',
            unique_together={('draft_session', 'rank', 'team')},
        ),
        migrations.AlterUniqueTogether(
            name='draftpick',
            unique_together={('pick_order', 'player', 'draft_session_rank')},
        ),
    ]