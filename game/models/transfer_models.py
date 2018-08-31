from django.db import models
from django.contrib.postgres.fields import JSONField
# import decimal
# import json
import pytz
import datetime
from datetime import timedelta

from ..models import league_models
from ligue1 import models as l1models


class MerkatoManager(models.Manager):

    def create_sessions(self, merkato):
        # create sessions
        ticks = [t for t in
                 MerkatoManager._generate_ticks(merkato.begin, merkato.end, merkato.configuration.get('closing_times'))]
        nb = 1
        for t in ticks:
            closing = t
            solving = closing + timedelta(hours=merkato.configuration.get('session_duration'))
            merkato.merkatosession_set.add(
                MerkatoSession.objects.create(merkato=merkato, number=nb, closing=closing, solving=solving))
            nb += 1
        return merkato

    @staticmethod
    def _generate_ticks(begin, end, closing_times):
        assert end >= begin
        delta = end - begin
        for d in range(delta.days + 1):
            for t in closing_times:
                tickday = begin + timedelta(days=d)
                dm = t.split(':')
                dt = tickday.replace(hour=int(dm[0]), minute=int(dm[1]), second=0)
                if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
                    yield dt
                else:
                    yield pytz.timezone('Europe/Paris').localize(dt)

    @staticmethod
    def _find_next_tick_to_close(date_from, duration, ticks):
        date_to = date_from + timedelta(hours=duration)
        # find the next tick _after_ date_to
        previous_tick = None
        for t in ticks:
            previous_tick = t
            if date_to <= t:
                break
        if date_to <= previous_tick:
            return previous_tick
        return None


class Merkato(models.Model):
    MODES = (('DRFT', 'Draft'), ('BID', 'Bid'))

    begin = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    mode = models.CharField(max_length=4, blank=False, choices=MODES)
    configuration = JSONField(blank=True)
    league_instance = models.ForeignKey(league_models.LeagueInstance, on_delete=models.CASCADE, null=False)

    objects = MerkatoManager()

    @staticmethod
    def _make_config(roster_size_max=9, sales_per_session=-1, pa_number=1, mv_number=1, mv_tax_rate=0.1,
                     re_tax_rate=0.5, initial_team_balance=100, closing_times=['10:00', '18:00'], session_duration=48):
        conf = {'roster_size_max': roster_size_max,
                'sales_per_session': sales_per_session,
                'pa_number': pa_number,
                'mv_number': mv_number,
                'mv_tax_rate': mv_tax_rate,
                're_tax_rate': re_tax_rate,
                'closing_times': closing_times,
                'session_duration': session_duration,
                'init_balance': initial_team_balance,
                'default_score_factor': 1.00
                }
        return conf

    def save(self, *args, **kwargs):
        if self.configuration is None:
            self.configuration = self._make_config()
        return super(Merkato, self).save(*args, **kwargs)


class MerkatoSessionManager(models.Manager):
    def get_next_available(self, merkato):
        now = datetime.datetime.now(pytz.utc)
        max_sales_in_session = merkato.configuration['sales_per_session']
        sess_gen = (s for s in self.filter(merkato=merkato).prefetch_related('sale_set').order_by('closing') if
                    s.closing >= now)
        for sess in sess_gen:
            if max_sales_in_session < 0:
                # first found is ok:
                return sess
            if len(sess.sale_set.all()) < max_sales_in_session:
                return sess
        return None


class MerkatoSession(models.Model):
    merkato = models.ForeignKey(Merkato, on_delete=models.CASCADE, null=False)
    number = models.PositiveIntegerField(blank=False)
    closing = models.DateTimeField(blank=False)
    solving = models.DateTimeField(blank=False)
    is_solved = models.BooleanField(null=False, default=False)
    attributes = JSONField(null=True)

    objects = MerkatoSessionManager()

    def __str__(self):
        return 'MerkatoSession #%d -> %s -> %s' % (self.number, self.closing, self.solving)

    def has_object_read_permission(self, request):
        return request.user in self.merkato.league_instance.league.members.all()

    def _make_attributes(self, score_factor=1.00):
        return {
            'score_factor': score_factor
        }

    def save(self, *args, **kwargs):
        if self.attributes is None:
            self.attributes = self._make_attributes()
        return super(MerkatoSession, self).save(*args, **kwargs)

    class Meta:
        ordering = ('closing',)


class SaleManager(models.Manager):
    def get_for_team(self, team, just_last_merkato=True, just_count=False, just_PA=True):
        qs = self.filter(team=team,
                         merkato_session__merkato__league_instance__current=True)
        if just_last_merkato:
            most_recent_merkato = Merkato.objects.filter(
                league_instance__league=league_models.Team.objects.get(pk=team.pk).league,
                league_instance__current=True,
                begin__lte=datetime.date.today()).order_by('-end').first()
            qs = qs.filter(merkato_session__merkato=most_recent_merkato)
        if just_PA:
            qs = qs.filter(type='PA')
        if just_count:
            return qs.count()
        else:
            return qs


class Sale(models.Model):
    TYPES = (('PA', 'Proposition d\'achat'), ('MV', 'Mise en vente'), ('AM', 'Achat masqué'))

    player = models.ForeignKey(l1models.Joueur, on_delete=models.CASCADE, null=False)
    team = models.ForeignKey(league_models.Team, on_delete=models.CASCADE, null=False)
    merkato_session = models.ForeignKey(MerkatoSession, on_delete=models.CASCADE, null=False)
    min_price = models.DecimalField(max_digits=4, decimal_places=1)
    type = models.CharField(max_length=2, blank=False, default='PA', choices=TYPES)
    winning_auction = models.ForeignKey('Auction', on_delete=models.SET_NULL, related_name='sale_won', null=True)
    rank = models.PositiveIntegerField(null=False, default=1)

    objects = SaleManager()

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
        if self.winning_auction:
            return self.winning_auction.value
        else:
            return self.min_price

    def get_selling_price(self):
        assert self.merkato_session.is_solved
        assert self.type == 'MV'
        assert self.winning_auction is not None
        return self.winning_auction.value * (
                1.0 - self.merkato_session.merkato.configuration['mv_tax_rate'])

    def get_winner_and_price(self):
        if self.winning_auction is None and self.type == 'PA':
            return self.team, self.min_price
        elif self.winning_auction is None and self.type == 'MV':
            return None, None
        else:
            return self.winning_auction.team, self.winning_auction.value

    class Meta:
        unique_together = (
            ('merkato_session', 'rank'),
            ('merkato_session', 'player'),
        )
        ordering = ('merkato_session', 'rank',)


class Auction(models.Model):
    REJECT_MOTIVES = (
        ('MONEY', 'Solde insuffisant'), ('MIN_PRICE', 'Enchère trop basse'), ('FULL', 'Plus de place dans l\'effectif'))

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=False, related_name='auctions')
    team = models.ForeignKey(league_models.Team, on_delete=models.CASCADE, null=False)
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
        available = float(self.team.bank_account.balance - self.team.bank_account.blocked)
        if self.sale.team.pk == self.team.pk:
            available += float(self.sale.min_price)
        current_session_won = Sale.objects.filter(merkato_session=self.sale.merkato_session,
                                                  rank__lt=self.sale.rank).filter(
            models.Q(winning_auction__team=self.team) |
            models.Q(winning_auction__isnull=True, team=self.team))
        current_spent = 0
        for csw in current_session_won:
            _, val = csw.get_winner_and_price()
            if val:
                current_spent += float(val)
        available -= current_spent
        if available < self.value:
            raise Auction.AuctionNotValidException(code='MONEY')
        # FULL
        current_roster_size = league_models.Signing.objects.filter(team=self.team,
                                                                   league_instance=league_models.LeagueInstance.objects.get_current(
                                                                       self.team.league),
                                                                   end__isnull=True).count()
        future_pa_locked = Sale.objects.filter(team=self.team).filter(
            models.Q(merkato_session__solving__gt=self.sale.merkato_session.solving) | models.Q(
                merkato_session=self.sale.merkato_session, rank__gt=self.sale.rank)).count()
        merkato_config = self.sale.merkato_session.merkato.configuration
        if current_roster_size + len(current_session_won) + future_pa_locked >= merkato_config['roster_size_max']:
            raise Auction.AuctionNotValidException(code='FULL')

    class Meta:
        unique_together = ('sale', 'team')


class ReleaseManager(models.Manager):
    def get_for_team(self, team, just_last_merkato=True, just_count=False):
        qs = self.filter(done=True, signing__team=team,
                         merkato_session__merkato__league_instance__current=True,
                         merkato_session__is_solved=True)
        if just_last_merkato:
            most_recent_merkato = Merkato.objects.filter(
                league_instance__league=(
                    team if isinstance(team, league_models.Team) else league_models.Team.objects.get(pk=team)).league,
                league_instance__current=True,
                begin__lte=datetime.date.today()).order_by('-end').first()
            qs = qs.filter(merkato_session__merkato=most_recent_merkato)
        if just_count:
            return qs.count()
        else:
            return qs.order_by('-signing__end')


class Release(models.Model):
    signing = models.ForeignKey(league_models.Signing, on_delete=models.CASCADE)
    merkato_session = models.ForeignKey(MerkatoSession, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=4, decimal_places=1)
    done = models.BooleanField(default=False)

    objects = ReleaseManager()
