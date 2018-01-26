from django.core.management.base import BaseCommand, CommandError
from game import models as gamemodels


class Command(BaseCommand):
    help = 'Fully recompute bank accounts and history since the beginning of the current league instance'

    def add_arguments(self, parser):
        parser.add_argument('league_id', nargs='+', type=int)

        parser.add_argument(
            '--start_amount',
            dest='start_amount',
            default=100,
            help='initial amount',
            type=int,
        )

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

            for team in gamemodels.Team.objects.filter(league=league):
                # init history
                history = list()
                gamemodels.BankAccountHistory init = gamemodels.BankAccountHistory()

        self.stdout.write('Done. %d league_instances processed' % licount)