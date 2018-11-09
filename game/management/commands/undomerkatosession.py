from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from game import models as gamemodels


class Command(BaseCommand):
    help = 'Revert a whole merkatosession'

    def add_arguments(self, parser):
        parser.add_argument('session_id', nargs=1, type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        session_id = options['session_id'][0]
        session = gamemodels.MerkatoSession.objects.get(pk=session_id)
        for s in gamemodels.Sale.objects.filter(merkato_session__pk=session_id):
            s.revert()  # TODO
            self.stdout.write('Sale %s reverted' % s)
        for r in gamemodels.Release.objects.filter(merkato_session__pk=session_id):
            r.revert()  # TODO
            self.stdout.write('Release %s reverted' % r)
        session.is_solved = False
        session.save()
        self.stdout.write('Session %s undone, recompute accounts...' % session_id)
        call_command('recomputeaccounts', session.merkato.league_instance.league.pk)
        self.stdout.write('Done.')
