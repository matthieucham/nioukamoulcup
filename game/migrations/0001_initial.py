# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-03 12:41
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ligue1', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='JJScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computed_at', models.DateTimeField(auto_now=True)),
                ('note', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('bonus', models.DecimalField(decimal_places=3, default=0, max_digits=5)),
                ('compensation', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('joueur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ligue1.Joueur')),
            ],
        ),
        migrations.CreateModel(
            name='JourneeScoring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('LOCKED', 'locked')], default='OPEN', max_length=10)),
                ('computed_at', models.DateTimeField(null=True)),
                ('locked_at', models.DateTimeField(null=True)),
                ('journee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ligue1.Journee')),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('official', models.BooleanField(default=False)),
                ('mode', models.CharField(choices=[('KCUP', 'Kamoulcup'), ('FSY', 'Fantasy')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueDivision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.PositiveSmallIntegerField()),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.League')),
                ('lower_division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='upper', to='game.LeagueDivision')),
                ('upper_division', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lower', to='game.LeagueDivision')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slogan', models.CharField(max_length=255)),
                ('current', models.BooleanField(default=False)),
                ('begin', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('configuration', django.contrib.postgres.fields.jsonb.JSONField()),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.League')),
                ('saison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ligue1.Saison')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueInstancePhase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('SEVEN', '7'), ('ELEVEN', '11')], max_length=10)),
                ('journee_first', models.PositiveIntegerField()),
                ('journee_last', models.PositiveIntegerField()),
                ('league_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.LeagueInstance')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueInstancePhaseDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('journee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ligue1.Journee')),
                ('league_instance_phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.LeagueInstancePhase')),
            ],
        ),
        migrations.CreateModel(
            name='LeagueMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_baboon', models.BooleanField(default=False)),
                ('date_joined', models.DateField()),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.League')),
            ],
        ),
        migrations.CreateModel(
            name='Merkato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('mode', models.CharField(choices=[('DRFT', 'Draft'), ('BID', 'Bid')], max_length=4)),
                ('configuration', django.contrib.postgres.fields.jsonb.JSONField()),
                ('league_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.LeagueInstance')),
            ],
        ),
        migrations.CreateModel(
            name='MerkatoSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('closing', models.DateTimeField()),
                ('result', django.contrib.postgres.fields.jsonb.JSONField()),
                ('merkato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Merkato')),
            ],
        ),
        migrations.CreateModel(
            name='SaisonScoring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computed_at', models.DateTimeField(auto_now=True)),
                ('saison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ligue1.Saison')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_price', models.DecimalField(decimal_places=1, max_digits=4)),
                ('type', models.CharField(choices=[('PA', "Proposition d'achat"), ('MV', 'Mise en vente'), ('AM', 'Achat masqué')], default='PA', max_length=2)),
                ('merkato_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.MerkatoSession')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ligue1.Joueur')),
            ],
        ),
        migrations.CreateModel(
            name='Signing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('is_current', models.BooleanField(default=True)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ligue1.Joueur')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField()),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.LeagueDivision')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.League')),
            ],
        ),
        migrations.CreateModel(
            name='TeamDayScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=3, max_digits=7)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.LeagueInstancePhaseDay')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Team')),
            ],
        ),
        migrations.AddField(
            model_name='signing',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Team'),
        ),
        migrations.AddField(
            model_name='sale',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Team'),
        ),
        migrations.AddField(
            model_name='leaguemembership',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='managers', to='game.Team'),
        ),
        migrations.AddField(
            model_name='leaguemembership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leagueinstancephaseday',
            name='results',
            field=models.ManyToManyField(through='game.TeamDayScore', to='game.Team'),
        ),
        migrations.AddField(
            model_name='league',
            name='members',
            field=models.ManyToManyField(related_name='leagues', through='game.LeagueMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='journeescoring',
            name='saison_scoring',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.SaisonScoring'),
        ),
        migrations.AddField(
            model_name='jjscore',
            name='journee_scoring',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.JourneeScoring'),
        ),
        migrations.AddField(
            model_name='auction',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to='game.Sale'),
        ),
        migrations.AddField(
            model_name='auction',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Team'),
        ),
    ]
