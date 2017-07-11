from django.db import models
from django.contrib.postgres.fields import JSONField

from ..models import league_models
from ligue1 import models as l1models
import decimal
import json
from datetime import timedelta


class MerkatoManager(models.Manager):
    def setup(self, league_instance, mode, begin, end, roster_size_max, closing_times=['12:00', '20:00'],
              session_duration=48):
        assert mode in ['BID', 'DRFT']
        Merkato = self.create(mode=mode, begin=begin, end=end, league_instance=league_instance,
                              configuration=self._make_config(roster_size_max, 10))
        # create sessions
        session_closing = begin + timedelta(hours=session_duration)
        # adjust session_closing time of the day to the next wanted closing hour:

    @staticmethod
    def _generate_ticks(begin, end, closing_times):
        assert end > begin
        delta = end - begin
        for d in range(delta.days + 1):
            for t in closing_times:
                tickday = begin + timedelta(days=d)
                dm = t.split(':')
                yield tickday.replace(hour=int(dm[0]), minute=int(dm[1]), second=0)

    @staticmethod
    def _find_next_tick_to_close(date_from, duration, ticks):
        date_to = date_from + timedelta(hours=duration)
        # find the next tick _after_ date_to
        previous_tick = None
        for t in ticks:
            previous_tick = t
            if date_to <= t:
                break
        return previous_tick


    def _make_config(self, roster_size_max, sales_per_session, pa_number=1, mv_number=1, mv_tax_rate=0.1,
                     re_tax_rate=0.5):
        return json.dumps(
            {'roster_size_max': roster_size_max, 'sales_per_session': sales_per_session, 'pa_number': pa_number,
             'mv_number': mv_number,
             'mv_tax_rate': mv_tax_rate, 're_tax_rate': re_tax_rate})


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