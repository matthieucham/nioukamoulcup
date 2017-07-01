from django.db import models
from django.contrib.postgres.fields import JSONField

from game import models as leaguemodels
from ligue1 import models as l1models


class Merkato(models.Model):
    MODES = (('DRFT', 'Draft'), ('BID', 'Bid'))

    begin = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    mode = models.CharField(max_length=4, blank=False, choices=MODES)
    configuration = JSONField()
    league_instance = models.ForeignKey(leaguemodels.LeagueInstance, null=False)


class MerkatoSession(models.Model):
    merkato = models.ForeignKey(Merkato, null=False)
    number = models.PositiveIntegerField(blank=False)
    closing = models.DateTimeField(blank=False)
    result = JSONField()


class Signing(models.Model):
    player = models.ForeignKey(l1models.Joueur, null=False)
    team = models.ForeignKey(leaguemodels.Team, null=False)
    date = models.DateField(blank=False)
    is_current = models.BooleanField(default=True)
    attributes = JSONField()


class Sale(models.Model):
    TYPES = (('PA', 'Proposition d\'achat'), ('MV', 'Mise en vente'), ('AM', 'Achat masqué'))

    player = models.ForeignKey(l1models.Joueur, null=False)
    team = models.ForeignKey(leaguemodels.Team, null=False)
    merkato_session = models.ForeignKey(MerkatoSession, null=False)
    min_price = models.DecimalField(max_digits=4, decimal_places=1)
    type = models.CharField(max_length=2, blank=False, default='PA', choices=TYPES)


class Auction(models.Model):
    sale = models.ForeignKey(Sale, null=False, related_name='auctions')
    team = models.ForeignKey(leaguemodels.Team, null=False)
    value = models.DecimalField(max_digits=4, decimal_places=1)