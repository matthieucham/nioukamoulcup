from django.db import models, transaction
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
import json

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


class Team(models.Model):
    name = models.CharField(max_length=100, blank=False)
    league = models.ForeignKey(League, null=False)
    division = models.ForeignKey(LeagueDivision)
    attributes = JSONField()


class BankAccountManager(models.Manager):
    @transaction.atomic
    def init_account(self, team, init_balance):
        account, created = self.get_or_create(team=team, defaults={'balance': init_balance, 'adjust': 0})
        if not created:
            account.balance = init_balance
            account.adjust = 0
            account.save()
        account.bankaccounthistory_set.clear()
        account.bankaccounthistory_set.add(
            BankAccountHistory.objects.create(amount=init_balance, new_balance=init_balance,
                                              info=BankAccountHistory.make_info_init()))

    @transaction.atomic
    def buy(self, team, amount, player):
        account = self.select_for_update().get(team=team)
        assert (account.balance + account.adjust + amount >= 0)  # amount is negative !
        account.balance += amount
        account.bank_account_history_set.add(
            BankAccountHistory.objects.create(amount=amount, new_balance=account.balance,
                                              info=BankAccountHistory.make_info_buy(player)))
        account.save()


class BankAccount(models.Model):
    team = models.OneToOneField(Team, primary_key=True, related_name='bank_account')
    balance = models.DecimalField(max_digits=4, decimal_places=1)
    adjust = models.DecimalField(max_digits=4, decimal_places=1)
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
    def make_info_buy(player):
        return json.dumps({'type': 'BUY', 'player_id': player.pk, 'player_name': player.__str__()})


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
    type = models.CharField(choices=TYPES, max_length=10)
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
