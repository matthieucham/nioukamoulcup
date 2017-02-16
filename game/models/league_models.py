from django.db import models
from ligue1 import models as l1models
from django.contrib.postgres.fields import JSONField


class League(models.Model):
    MODES = (('KCUP', 'Kamoulcup'), ('FSY', 'Fantasy'))
    name = models.CharField(max_length=100, blank=False)
    official = models.BooleanField(default=False)
    mode = models.CharField(max_length=4, choices=MODES)


class LeagueDivision(models.Model):
    league = models.ForeignKey(League, null=False)
    level = models.PositiveSmallIntegerField(null=False)
    name = models.CharField(max_length=100, blank=False)
    capacity = models.PositiveSmallIntegerField()
    upper_division = models.ForeignKey("self")
    lower_division = models.ForeignKey("self")


class Team(models.Model):
    name = models.CharField(max_length=100, blank=False)
    league = models.ForeignKey(League, null=False)
    division = models.ForeignKey(LeagueDivision)


class LeagueInstance(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slogan = models.CharField(max_length=255)
    league = models.ForeignKey(League, null=False)
    current = models.BooleanField(default=False)
    begin = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    saison = models.ForeignKey(l1models.Saison)
    configuration = JSONField()


class LeagueInstancePhase(models.Model):
    TYPES = (('SEVEN', '7'), ('ELEVEN', '11'))

    league_instance = models.ForeignKey(LeagueInstance, null=False)
    name = models.CharField(max_length=100)
    type = models.CharField(choices=TYPES)
    journee_first = models.PositiveIntegerField(blank=False)
    journee_last = models.PositiveIntegerField(blank=False)


class LeagueInstancePhaseDay(models.Model):
    league_instance_phase = models.ForeignKey(LeagueInstancePhase, null=False)
    number = models.PositiveIntegerField(blank=False)
    journee = models.ForeignKey(l1models.Journee, null=False)
    results = models.ManyToManyField(Team, through='TeamDayScore')


class TeamDayScore(models.Model):
    day = models.ForeignKey(LeagueInstancePhaseDay, null=False)
    team = models.ForeignKey(Team)
    score = models.DecimalField(decimal_places=3, max_digits=7)


class Merkato(models.Model):
    MODES = (('DRFT', 'Draft'), ('BID', 'Bid'))

    begin = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    mode = models.CharField(max_length=4, blank=False, choices=MODES)
    configuration = JSONField()
    league_instance = models.ForeignKey(LeagueInstance, null=False)


class MerkatoSession(models.Model):
    merkato = models.ForeignKey(Merkato, null=False)
    number = models.PositiveIntegerField(blank=False)
    closing = models.DateTimeField(blank=False)
