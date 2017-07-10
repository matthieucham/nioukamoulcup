from django.db import models
from django.contrib.postgres.fields import JSONField

from ..models import league_models
from ligue1 import models as l1models
import decimal


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


class Sale(models.Model):
    TYPES = (('PA', 'Proposition d\'achat'), ('MV', 'Mise en vente'), ('AM', 'Achat masqué'))

    player = models.ForeignKey(l1models.Joueur, null=False)
    team = models.ForeignKey(league_models.Team, null=False)
    merkato_session = models.ForeignKey(MerkatoSession, null=False)
    min_price = models.DecimalField(max_digits=4, decimal_places=1)
    type = models.CharField(max_length=2, blank=False, default='PA', choices=TYPES)
    winning_auction = models.ForeignKey('Auction', related_name='sale_won', null=True)
    rank = models.PositiveIntegerField(null=False, default=1)

    def save(self, *args, **kwargs):
        """
        Call Sale create operations within LockedAtomicTransaction
        """
        if not self.pk:
            # set rank as max rank of session +1
            try:
                max_rank_sale = Sale.objects.filter(merkato_session=self.merkato_session).latest('rank')
                self.rank = max_rank_sale.rank + 1
            except Sale.DoesNotExist:
                self.rank = 1
        super(Sale, self).save(*args, **kwargs)

    def get_buying_price(self):
        assert self.merkato_session.is_solved
        if self.winning_auction:
            return self.winning_auction.value
        else:
            assert self.type == 'PA'
            return self.min_price

    def get_selling_price(self):
        assert self.merkato_session.is_solved
        assert self.type == 'MV'
        assert self.winning_auction is not None
        # TODO apply factor from self.merkato_session.merkato.config
        return self.winning_auction.value

    class Meta:
        unique_together = (
            ('merkato_session', 'rank'),
            ('merkato_session', 'player'),
        )
        ordering = ('merkato_session', 'rank', )


class Auction(models.Model):
    REJECT_MOTIVES = (
        ('MONEY', 'Solde insuffisant'), ('MIN_PRICE', 'Enchère trop basse'), ('FULL', 'Plus de place dans l\'effectif'))

    sale = models.ForeignKey(Sale, null=False, related_name='auctions')
    team = models.ForeignKey(league_models.Team, null=False)
    value = models.DecimalField(max_digits=4, decimal_places=1)
    is_valid = models.NullBooleanField(null=True)
    reject_cause = models.CharField(max_length=10, null=True)

    class AuctionNotValidException(Exception):
        def __init__(self, code):
            super(Exception, self).__init__()
            self.code = code

    def validate(self):
        # MIN_PRICE
        if self.sale.type == 'MV':
            if self.sale.min_price > self.value:
                raise Auction.AuctionNotValidException(code='MIN_PRICE')
        else:
            if self.sale.min_price >= self.value:
                raise Auction.AuctionNotValidException(code='MIN_PRICE')
        # MONEY
        available = decimal.Decimal(self.team.bank_account.balance - self.team.bank_account.blocked)
        if self.sale.team.pk == self.team.pk:
            available += decimal.Decimal(self.sale.min_price)
        if available < self.value:
            raise Auction.AuctionNotValidException(code='MONEY')
        # TODO FULL

    class Meta:
        unique_together = ('sale', 'team')


class Release(models.Model):
    signing = models.ForeignKey(league_models.Signing)
    merkato_session = models.ForeignKey(MerkatoSession)
    amount = models.DecimalField(max_digits=4, decimal_places=1)
    done = models.BooleanField(default=False)