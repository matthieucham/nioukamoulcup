from django.db import models, transaction
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
import json
from collections import defaultdict

from . import scoring_models
from ligue1 import models as l1models


class League(models.Model):
    MODES = (('KCUP', 'Kamoulcup'), ('FSY', 'Fantasy'))
    name = models.CharField(max_length=100, blank=False)
    official = models.BooleanField(default=False)
    mode = models.CharField(max_length=4, choices=MODES)
    members = models.ManyToManyField(User, through='LeagueMembership', related_name='leagues')


class LeagueMembership(models.Model):
    user = models.ForeignKey(User)
    league = models.ForeignKey(League)
    is_baboon = models.BooleanField(default=False)
    date_joined = models.DateField()
    team = models.ForeignKey('Team', related_name='managers', null=True)


class LeagueDivision(models.Model):
    league = models.ForeignKey(League, null=False)
    level = models.PositiveSmallIntegerField(null=False)
    name = models.CharField(max_length=100, blank=False)
    capacity = models.PositiveSmallIntegerField()
    upper_division = models.ForeignKey("self", related_name='lower', null=True)
    lower_division = models.ForeignKey("self", related_name='upper', null=True)


class TeamManager(models.Manager):
    def setup_formation(self, team, g=1, d=2, m=2, a=2):
        t = self.select_for_update().get(pk=team.pk)
        json.loads(t.attributes)['formation'] = {'G': g, 'D': d, 'M': m, 'A': a}
        t.save()  # todo update score

    def setup_joker(self, team, joueur):
        assert Signing.objects.filter(player=joueur, team=team, end__isnull=True) is not None
        t = self.select_for_update().get(pk=team.pk)
        json.loads(t.attributes)['joker'] = joueur.pk
        t.save()


class Team(models.Model):
    name = models.CharField(max_length=100, blank=False)
    league = models.ForeignKey(League, null=False)
    division = models.ForeignKey(LeagueDivision)
    attributes = JSONField()

    objects = TeamManager


class BankAccountManager(models.Manager):
    @transaction.atomic()
    def init_account(self, team, init_balance):
        account, created = self.get_or_create(team=team, defaults={'balance': init_balance, 'blocked': 0})
        if not created:
            account.balance = init_balance
            account.blocked = 0
            account.save()
        account.bankaccounthistory_set.clear()
        account.bankaccounthistory_set.add(
            BankAccountHistory.objects.create(amount=init_balance, new_balance=init_balance,
                                              info=BankAccountHistory.make_info_init()))

    @transaction.atomic()
    def buy(self, sale):
        if sale.winning_auction is not None:
            buyer = sale.winning_auction.team
        else:
            buyer = sale.team
        account = self.select_for_update().get(team=buyer)
        amount = sale.get_buying_price()
        assert (account.balance - amount >= 0)
        account.balance -= amount
        account.bankaccounthistory_set.add(
            BankAccountHistory.objects.create(amount=amount, new_balance=account.balance,
                                              info=BankAccountHistory.make_info_buy(sale.player,
                                                                                    seller=sale.team if sale.type == 'MV' else None)))
        account.save()

    @transaction.atomic()
    def release(self, release_item):
        account = self.select_for_update().get(team=release_item.signing.team)
        account.balance += release_item.amount
        account.bankaccounthistory_set.add(
            BankAccountHistory.objects.create(amount=release_item.amount, new_balance=account.balance,
                                              info=BankAccountHistory.make_info_release(release_item.signing.player)))
        account.save()

    @transaction.atomic()
    def sell(self, sale):
        assert (sale.type == 'MV')
        assert (sale.winning_auction is not None)
        amount = sale.get_selling_price()
        assert (amount >= sale.min_price)
        account = self.select_for_update().get(team=sale.winning_auction.team)
        assert (account.balance - amount >= 0)
        account.balance -= amount
        account.bankaccounthistory_set.add(
            BankAccountHistory.objects.create(amount=amount, new_balance=account.balance,
                                              info=BankAccountHistory.make_info_sell(sale.player,
                                                                                     sale.team)))
        account.save()


class BankAccount(models.Model):
    team = models.OneToOneField(Team, primary_key=True, related_name='bank_account')
    balance = models.DecimalField(max_digits=4, decimal_places=1)
    blocked = models.DecimalField(max_digits=4, decimal_places=1)
    objects = BankAccountManager()


class BankAccountHistory(models.Model):
    bank_account = models.ForeignKey(BankAccount, null=True)  # entries with null ref will be deleted by batch
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=4, decimal_places=1)
    new_balance = models.DecimalField(max_digits=4, decimal_places=1)
    info = JSONField()

    @staticmethod
    def make_info_init():
        return json.dumps({'type': 'INIT'})

    @staticmethod
    def make_info_buy(player, seller=None):
        return json.dumps({'type': 'BUY', 'player_id': player.pk, 'player_name': player.__str__(),
                           'seller_name': seller.name if seller else None})

    @staticmethod
    def make_info_sell(player, buyer):
        return json.dumps({'type': 'SELL', 'player_id': player.pk, 'player_name': player.__str__(),
                           'buyer_name': buyer.name})

    @staticmethod
    def make_info_release(player):
        return json.dumps({'type': 'RELEASE', 'player_id': player.pk, 'player_name': player.__str__()})


class LeagueInstance(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slogan = models.CharField(max_length=255)
    league = models.ForeignKey(League, null=False)
    current = models.BooleanField(default=False)
    begin = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    saison = models.ForeignKey(l1models.Saison)
    configuration = JSONField(default=dict([('notes', [('SEVEN', 13), ('ELEVEN', 26)])]))


class LeagueInstancePhase(models.Model):
    TYPES = (('SEVEN', '7'), ('ELEVEN', '11'))

    league_instance = models.ForeignKey(LeagueInstance, null=False)
    name = models.CharField(max_length=100)
    type = models.CharField(choices=TYPES, max_length=10)
    journee_first = models.PositiveIntegerField(blank=False)
    journee_last = models.PositiveIntegerField(blank=False)

    class Meta:
        unique_together = (('league_instance', 'journee_first',), ('league_instance', 'journee_last'),)


class LeagueInstancePhaseDayManager(models.Manager):
    def compute_results(self, league_instance, journee):
        # find the phase
        phases = LeagueInstancePhase.object.filter(league_instance=league_instance, journee_first__lte=journee.numero,
                                                   journee_last_gte=journee.numero)
        for ph in phases:
            lipd, created = self.select_related().get_or_create(league_instance_phase=ph, journee=journee,
                                                                defaults={'number': journee.numero})
            team_day_scores = self._compute_scores_for_phaseday(lipd)
            if created:
                TeamDayScore.objects.bulk_create(team_day_scores)
            else:
                for tds in team_day_scores:
                    tds.save()

    def _compute_scores_for_phaseday(self, lipd):
        return [self._compute_teamdayscore(team, lipd) for team in
                Team.objects.filter(league=lipd.league_instance_phase.league_instance.league).prefetch_related(
                    'signing_set')]

    def _compute_teamdayscore(self, team, lipd):
        league_mode = lipd.league_instance_phase.league_instance.league.mode
        team_config = json.loads(team.attributes)
        if league_mode == 'KCUP':
            jjscore_max_nb = json.loads(lipd.league_instance_phase.league_instance.configuration)['notes'][
                lipd.league_instance_phase.type]
            # filter signings valid at this time
            signings_at_day = [s for s in team.signing_set if
                               (s.begin <= lipd.journee.debut) and (s.end is None or s.end > lipd.journee.debut)]
            # retrieve jjscores for all signings at once in order to limit the number of request
            all_jjscores = scoring_models.JJScore.objects.filter(
                journee_scoring__saison_scoring__saison=lipd.league_instance_phase.league_instance.saison,
                journee_scoring__journee__numero__gte=lipd.league_instance_phase.journee_first,
                journee_scoring__journee__numero__lte=lipd.journee.numero,
                joueur__in=[s.player.pk for s in signings_at_day]
            ).select_related('joueur').order_by('joueur')
            dscores = defaultdict(list)
            for jjs in all_jjscores:
                dscores[jjs.pk].append(jjs)
            for jjspk in dscores:
                score = self._compute_score_player(dscores[jjspk], jjscore_max_nb, )
        else:
            # TODO
            return None

    def _compute_score_player(self, jjslist):



class LeagueInstancePhaseDay(models.Model):
    league_instance_phase = models.ForeignKey(LeagueInstancePhase, null=False)
    number = models.PositiveIntegerField(blank=False)
    journee = models.ForeignKey(l1models.Journee, null=False)
    results = models.ManyToManyField(Team, through='TeamDayScore', null=True)


class TeamDayScore(models.Model):
    day = models.ForeignKey(LeagueInstancePhaseDay, null=False)
    team = models.ForeignKey(Team)
    score = models.DecimalField(decimal_places=3, max_digits=7)
    attributes = JSONField()


class Signing(models.Model):
    player = models.ForeignKey(l1models.Joueur, null=False)
    team = models.ForeignKey(Team, null=False)
    begin = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)
    attributes = JSONField()