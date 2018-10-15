from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from game import models as gamemodels
from game.services import auctions
from django.utils import timezone


class Command(BaseCommand):
    help = 'Solve merkato and draft sessions when finished'

    @transaction.atomic
    def handle(self, *args, **options):
        self._solve_drafts()
        self._solve_merkatos()

    def _solve_drafts(self):
        for ds in gamemodels.DraftSession.objects.filter(merkato__league_instance__current=True,
                                                         merkato__mode='DRFT',
                                                         closing__lt=timezone.now(),
                                                         is_solved=False):
            self.stdout.write('Solving draft session #%s ...' % ds.pk)
            auctions.solve_draft_session(ds)
            self.stdout.write('Done')
        self.stdout.write('_solve_drafts completed.')

    def _solve_merkatos(self):
        for ms in gamemodels.MerkatoSession.objects.filter(merkato__league_instance__current=True,
                                                           merkato__mode='BID',
                                                           solving__lt=timezone.now(),
                                                           is_solved=False):
            self.stdout.write('Solving merkato session #%s ...' % ms.pk)
            auctions.solve_session(ms)
            auctions.apply_transfers(ms)
            self.stdout.write('Done')
        self.stdout.write('_solve_merkatos completed.')
