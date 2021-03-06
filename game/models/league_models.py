from django.db import models, transaction
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
# import json
from collections import defaultdict
import datetime

from . import scoring_models
from ligue1 import models as l1models
from utils.timer import Timer
from django.utils import timezone


class League(models.Model):
    MODES = (('KCUP', 'Kamoulcup'), ('FSY', 'Fantasy'))
    name = models.CharField(max_length=100, blank=False)
    official = models.BooleanField(default=False)
    mode = models.CharField(max_length=4, choices=MODES)
    members = models.ManyToManyField(User, through='LeagueMembership', related_name='leagues')

    def has_object_read_permission(self, request):
        return request.user in self.members.all()


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

    def __str__(self):
        return self.name


class TeamManager(models.Manager):
    @transaction.atomic()
    def setup_formation(self, team, g=1, d=2, m=2, a=2):
        t = self.select_for_update().get(pk=team.pk)
        team_config = t.attributes
        team_config['formation'] = {'G': g, 'D': d, 'M': m, 'A': a}
        t.attributes = team_config
        t.save()  # todo update score

    @transaction.atomic()
    def setup_joker(self, team, joueur):
        assert Signing.objects.filter(player=joueur, team=team, end__isnull=True) is not None
        t = self.select_for_update().get(pk=team.pk)
        team_config = t.attributes['joker'] = joueur.pk
        t.attributes = team_config
        t.save()


class Team(models.Model):
    name = models.CharField(max_length=100, blank=False)
    league = models.ForeignKey(League, null=False)
    division = models.ForeignKey(LeagueDivision)
    attributes = JSONField()

    objects = TeamManager()

    def has_object_read_permission(self, request):
        return request.user in self.league.members.all()

    def has_object_write_permission(self, request):
        return LeagueMembership.objects.filter(user=request.user, team=self).count() > 0

    def __str__(self):
        return self.name


class BankAccountManager(models.Manager):
    @transaction.atomic()
    def init_account(self, date, team, init_balance):
        account, created = self.get_or_create(team=team, defaults={'balance': init_balance, 'blocked': 0})
        if not created:
            account.balance = init_balance
            account.blocked = 0
            account.save()
        account.bankaccounthistory_set.add(
            BankAccountHistory.objects.create(date=date, amount=init_balance, new_balance=init_balance,
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
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=4, decimal_places=1)
    new_balance = models.DecimalField(max_digits=4, decimal_places=1)
    info = JSONField()

    @staticmethod
    def make_info_init():
        return {'type': 'INIT'}

    @staticmethod
    def make_info_buy(player, seller=None):
        return {'type': 'BUY', 'player_id': player.pk, 'player_name': player.display_name(),
                'seller_name': seller.name if seller else None}

    @staticmethod
    def make_info_sell(player, buyer):
        return {'type': 'SELL', 'player_id': player.pk, 'player_name': player.display_name(),
                'buyer_name': buyer.name}

    @staticmethod
    def make_info_release(player):
        return {'type': 'RELEASE', 'player_id': player.pk, 'player_name': player.display_name()}


class LeagueInstance(models.Model):
    name = models.CharField(max_length=100, blank=False)
    slogan = models.CharField(max_length=255)
    league = models.ForeignKey(League, null=False)
    current = models.BooleanField(default=False)
    begin = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
    saison = models.ForeignKey(l1models.Saison)
    configuration = JSONField(
        default=dict({'notes': {'HALFSEASON': 13, 'FULLSEASON': 26, 'TOURNAMENT': 3}}))

    def has_object_read_permission(self, request):
        return request.user in self.league.members.all()


class LeagueInstancePhase(models.Model):
    TYPES = (('HALFSEASON', 'Half season'), ('FULLSEASON', 'Whole season'), ('TOURNAMENT', 'Tournament'))

    league_instance = models.ForeignKey(LeagueInstance, null=False)
    name = models.CharField(max_length=100)
    type = models.CharField(choices=TYPES, max_length=10)
    journee_first = models.PositiveIntegerField(blank=False, db_index=True)
    journee_last = models.PositiveIntegerField(blank=False, db_index=True)


class LeagueInstancePhaseDayManager(models.Manager):
    def compute_results(self, league_instance, journee):
        with Timer(id='compute_results', verbose=True):
            # find the phase
            phases = LeagueInstancePhase.objects.filter(league_instance=league_instance,
                                                        journee_first__lte=journee.numero,
                                                        journee_last__gte=journee.numero)
            for ph in phases:
                lipd, created = self.get_or_create(league_instance_phase=ph, journee=journee,
                                                   defaults={'number': journee.numero})
                team_day_scores = self._compute_scores_for_phaseday(lipd)
                if not created:
                    TeamDayScore.objects.filter(day=lipd).delete()  # delete existing and recompute.
                TeamDayScore.objects.bulk_create(team_day_scores)

    def _compute_scores_for_phaseday(self, lipd):
        return [self._compute_teamdayscore(team, lipd) for team in
                Team.objects.filter(league=lipd.league_instance_phase.league_instance.league).prefetch_related(
                    'signing_set')]

    def _compute_teamdayscore(self, team, lipd):
        league_mode = lipd.league_instance_phase.league_instance.league.mode
        # filter signings valid at this time
        signings_at_day = [s for s in team.signing_set.all() if
                           (s.begin <= lipd.journee.debut) and (s.end is None or s.end > lipd.journee.debut)]
        if league_mode == 'KCUP':
            jjscore_max_nb = lipd.league_instance_phase.league_instance.configuration['notes'][
                lipd.league_instance_phase.type]
            try:
                existing_tds = TeamDayScore.objects.get(day=lipd, team=team)
                tds_config = existing_tds.attributes
                joker = tds_config['joker'] if 'joker' in tds_config else None
                formation = tds_config['formation']
            except TeamDayScore.DoesNotExist:  # joker and formation mustn't be modified afterwards
                team_config = team.attributes
                joker = team_config['joker'] if 'joker' in team_config else None
                formation = team_config['formation']
            signings_scores = [
                (signing, self._compute_score_signing_KCUP(lipd, signing, formation, jjscore_max_nb, joker))
                for signing in signings_at_day]
            dscores = defaultdict(list)
            for sig, sco in signings_scores:
                dscores[sig.player.poste].append((sig, sco))
            teamscore = 0
            composition = defaultdict(list)
            for poste in formation:
                scores_at_poste = sorted(dscores[poste], key=lambda x: x[1], reverse=True)
                for i in range(0, len(scores_at_poste)):
                    if i < formation[poste]:
                        teamscore += scores_at_poste[i][1]
                    composition[poste].append(scores_at_poste[i])
            return self._make_teamdayscore(team, lipd, teamscore, composition)
        else:
            # TODO
            return None

    def _compute_score_signing_KCUP(self, lipd, signing, formation, jjscore_max_nb, joker):
        jjscores = scoring_models.JJScore.objects.filter(
            journee_scoring__saison_scoring__saison=lipd.league_instance_phase.league_instance.saison,
            journee_scoring__journee__numero__gte=lipd.league_instance_phase.journee_first,
            journee_scoring__journee__numero__lte=lipd.journee.numero,
            joueur=signing.player
        ).annotate(no_note=models.Count('note')).annotate(no_comp=models.Count('compensation')).order_by('-no_note',
                                                                                                         '-note',
                                                                                                         '-no_comp',
                                                                                                         '-compensation')  # to have real notes first and compensations last
        nb_notes = 0
        score = 0
        factor = 1.0
        if 'score_factor' in signing.attributes:
            factor = signing.attributes['score_factor']
        for jjs in jjscores:
            base = jjs.bonus
            extra_bonus = 0
            if joker and joker == jjs.joueur.pk:
                extra_bonus = jjs.bonus  # doubled bonus
            if jjs.note is not None and nb_notes < jjscore_max_nb:
                base += jjs.note
            elif jjs.compensation is not None and nb_notes < jjscore_max_nb:
                base += jjs.compensation
            nb_notes += 1
            score += (float(base) * factor) + float(extra_bonus)
        return score

    def _make_teamdayscore(self, team, lipd, teamscore, composition):
        attrs = dict()
        attrs['composition'] = {}
        for poste, _ in l1models.Joueur.POSTES:
            attrs['composition'][poste] = [
                {'player': {'id': sig.player.pk, 'name': sig.player.display_name()},
                 'club': {'id': sig.player.club.pk, 'name': sig.player.club.nom} if sig.player.club else None,
                 'score': round(sco, 2),
                 'score_factor': sig.attributes['score_factor'] if 'score_factor' in sig.attributes else 1.0} for
                sig, sco in composition[poste]]
        team_config = team.attributes
        if 'joker' in team_config:
            attrs['joker'] = team_config['joker']
        attrs['formation'] = team_config['formation']
        return TeamDayScore(team=team, day=lipd, score=teamscore, attributes=attrs)

    def get_latest_day_for_phases(self, phases):
        latest_days = []
        for ph in phases:
            latest_day = self.filter(league_instance_phase=ph,
                                     results__isnull=False).prefetch_related('teamdayscore_set').order_by(
                '-number').first()
            if latest_day:
                latest_days.append(latest_day)
        return latest_days


class LeagueInstancePhaseDay(models.Model):
    league_instance_phase = models.ForeignKey(LeagueInstancePhase, null=False)
    number = models.PositiveIntegerField(blank=False)
    journee = models.ForeignKey(l1models.Journee, null=False)
    results = models.ManyToManyField(Team, through='TeamDayScore')

    objects = LeagueInstancePhaseDayManager()

    class Meta:
        ordering = ['journee']


class TeamDayScore(models.Model):
    day = models.ForeignKey(LeagueInstancePhaseDay, null=False)
    team = models.ForeignKey(Team)
    score = models.DecimalField(decimal_places=3, max_digits=7)
    attributes = JSONField()

    class Meta:
        ordering = ['-day']


class SigningManager(models.Manager):

    def end(self, signing, reason, date=timezone.now(), amount=None):
        if signing.end:
            raise ValueError('Cannot end a signing which has a end date already')
        if reason not in ('RE', 'MV', 'FR'):
            raise ValueError('reason must be on of RE (release), MV (sold), FR (freed)')
        signing.end = date
        signing.attributes['end_reason'] = reason
        if amount:
            signing.attributes['end_amount'] = amount
        self.update(signing)


class Signing(models.Model):
    player = models.ForeignKey(l1models.Joueur, null=False)
    team = models.ForeignKey(Team, null=False)
    begin = models.DateTimeField(auto_now_add=True, db_index=True)
    end = models.DateTimeField(null=True, db_index=True)
    attributes = JSONField(default=dict({'score_factor': 1.0}))

    objects = SigningManager()
