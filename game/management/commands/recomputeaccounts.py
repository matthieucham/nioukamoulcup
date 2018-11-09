from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from game import models as gamemodels
import decimal


class Command(BaseCommand):
    help = 'Fully recompute bank accounts and history since the beginning of the current league instance'

    def add_arguments(self, parser):
        parser.add_argument('league_id', nargs='+', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        for league_id in options['league_id']:
            try:
                league = gamemodels.League.objects.get(pk=league_id)
                instance = gamemodels.LeagueInstance.objects.get(league=league, current=True)
            except gamemodels.League.DoesNotExist:
                raise CommandError('League %s does not exist' % league_id)
            except gamemodels.LeagueInstance.DoesNotExist:
                raise CommandError('League %s has no current instance' % league_id)
            except gamemodels.LeagueInstance.MultipleObjectsReturned:
                raise CommandError('League %s has multiple current instances !' % league_id)

            # clear previous history
            gamemodels.BankAccountHistory.objects.filter(bank_account__team__league=league).delete()
            # get all budget-related events
            events = list()
            for mkt in gamemodels.Merkato.objects.filter(league_instance=instance):
                if 'init_balance' in mkt.configuration:
                    for t in gamemodels.Team.objects.filter(league=league):
                        events.append({'date': mkt.begin, 'merkato': mkt,
                                       'team': t})
            for sales_pa in gamemodels.Sale.objects.filter(type='PA',
                                                           merkato_session__is_solved=True,
                                                           merkato_session__merkato__league_instance=instance).select_related(
                'winning_auction').select_related('merkato_session'):
                events.append({'date': sales_pa.merkato_session.solving,
                               'team': sales_pa.winning_auction.team if sales_pa.winning_auction else sales_pa.team,
                               'debit': - sales_pa.get_buying_price(),
                               'sale': sales_pa})
            for sales_mv in gamemodels.Sale.objects.filter(type='MV',
                                                           merkato_session__is_solved=True,
                                                           merkato_session__merkato__league_instance=instance).select_related(
                'winning_auction').select_related('merkato_session'):
                if sales_mv.winning_auction:
                    events.append({'date': sales_mv.merkato_session.solving,
                                   'team': sales_mv.winning_auction.team,
                                   'debit': - sales_mv.winning_auction.value,
                                   'sale': sales_mv})
                    events.append({'date': sales_mv.merkato_session.solving,
                                   'team': sales_mv.team,
                                   'credit': sales_mv.winning_auction.value * decimal.Decimal(
                                       1.0 - sales_mv.merkato_session.merkato.configuration[
                                           'mv_tax_rate']) if 'mv_tax_rate' in sales_mv.merkato_session.merkato.configuration else sales_mv.winning_auction.value,
                                   'sale': sales_mv})

            for re in gamemodels.Release.objects.select_related('signing').select_related('merkato_session').filter(
                    merkato_session__is_solved=True,
                    merkato_session__merkato__league_instance=instance, done=True):
                events.append({'date': re.merkato_session.solving,
                               'team': re.signing.team,
                               'credit': re.amount,
                               'release': re})
            for ev in sorted(sorted(events, key=lambda e: 0 if 'release' in e else 1), key=lambda e: e['date']):
                account = gamemodels.BankAccount.objects.get(team=ev['team'])
                if 'merkato' in ev:
                    mkt = ev['merkato']
                    account.balance = decimal.Decimal(mkt.configuration['init_balance'])
                    account.bankaccounthistory_set.add(
                        gamemodels.BankAccountHistory.objects.create(date=ev['date'], amount=account.balance,
                                                                     new_balance=account.balance,
                                                                     info=gamemodels.BankAccountHistory.make_info_init(
                                                                         mkt)))
                    account.save()
                if 'debit' in ev:
                    account.balance += ev['debit']
                    account.bankaccounthistory_set.add(
                        gamemodels.BankAccountHistory.objects.create(amount=ev['debit'],
                                                                     new_balance=account.balance,
                                                                     date=ev['date'],
                                                                     info=gamemodels.BankAccountHistory.make_info_buy(
                                                                         ev['sale'].player,
                                                                         seller=ev['sale'].team if ev[
                                                                                                       'sale'].type == 'MV' else None)))
                    account.save()
                if 'credit' in ev:
                    account.balance += ev['credit']
                    if 'sale' in ev:
                        info = gamemodels.BankAccountHistory.make_info_sell(ev['sale'].player,
                                                                            buyer=ev['sale'].winning_auction.team)
                    elif 'release' in ev:
                        info = gamemodels.BankAccountHistory.make_info_release(ev['release'].signing.player)
                    account.bankaccounthistory_set.add(
                        gamemodels.BankAccountHistory.objects.create(date=ev['date'], amount=ev['credit'],
                                                                     new_balance=account.balance,
                                                                     info=info))
                    account.save()
                # TODO block current PA values
            self.stdout.write('League instance %d done.' % league_id)
