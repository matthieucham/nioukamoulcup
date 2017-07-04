from django.db import models
from django.contrib.postgres.fields import JSONField

from ..models import league_models
from ligue1 import models as l1models


class Merkato(models.Model):
    MODES = (('DRFT', 'Draft'), ('BID', 'Bid'))

    begin = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    mode = models.CharField(max_length=4, blank=False, choices=MODES)
    configuration = JSONField()
    league_instance = models.ForeignKey(league_models.LeagueInstance, null=False)


class MerkatoSession(models.Model):
    merkato = models.ForeignKey(Merkato, null=False)
    number = models.PositiveIntegerField(blank=False)
    closing = models.DateTimeField(blank=False)
    is_solved = models.BooleanField(null=False, default=False)


class Signing(models.Model):
    player = models.ForeignKey(l1models.Joueur, null=False)
    team = models.ForeignKey(league_models.Team, null=False)
    date = models.DateField(blank=False)
    is_current = models.BooleanField(default=True)
    attributes = JSONField()


class Sale(models.Model):
    TYPES = (('PA', 'Proposition d\'achat'), ('MV', 'Mise en vente'), ('AM', 'Achat masqué'))

    player = models.ForeignKey(l1models.Joueur, null=False)
    team = models.ForeignKey(league_models.Team, null=False)
    merkato_session = models.ForeignKey(MerkatoSession, null=False)
    min_price = models.DecimalField(max_digits=4, decimal_places=1)
    type = models.CharField(max_length=2, blank=False, default='PA', choices=TYPES)
    winning_auction = models.ForeignKey('Auction', related_name='sale_won', null=True)


class Auction(models.Model):
    REJECT_MOTIVES = (
        ('MONEY', 'Solde insuffisant'), ('MIN_PRICE', 'Enchère trop basse'), ('FULL', 'Plus de place dans l\'effectif'))

    sale = models.ForeignKey(Sale, null=False, related_name='auctions')
    team = models.ForeignKey(league_models.Team, null=False)
    value = models.DecimalField(max_digits=4, decimal_places=1)
    is_valid = models.NullBooleanField(null=True)
    reject_cause = models.CharField(max_length=10, null=True)

    class Meta:
        unique_together = ('sale', 'team')