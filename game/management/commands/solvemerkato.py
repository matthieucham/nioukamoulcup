from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from game import models as gamemodels
from game.services import auctions
from django.utils import timezone
from utils.cache_expensive_functions import flush_cache


class Command(BaseCommand):
    help = 'Solve merkato and draft sessions when finished'

    @transaction.atomic
    def handle(self, *args, **options):
        self._solve_drafts()
        self._solve_merkatos()
        # Recalculer le score courant est nécessaire car les effectifs ont changé
        for instance in gamemodels.LeagueInstance.objects.filter(current=True):
            gamemodels.LeagueInstancePhaseDay.objects.compute_current_results(instance)
            self.stdout.write('current score of %s computed.' % instance)

    def _solve_drafts(self):
        for ds in gamemodels.DraftSession.objects.filter(merkato__league_instance__current=True,
                                                         merkato__mode='DRFT',
                                                         closing__lt=timezone.now(),
                                                         is_solved=False).order_by('number'):
            self.stdout.write('Solving draft session #%s ...' % ds.pk)
            auctions.solve_draft_session(ds)
            self.stdout.write('Done')
            flush_cache()
        self.stdout.write('_solve_drafts completed.')

    def _solve_merkatos(self):
        for ms in gamemodels.MerkatoSession.objects.filter(merkato__league_instance__current=True,
                                                           merkato__mode='BID',
                                                           solving__lt=timezone.now(),
                                                           is_solved=False).order_by('number'):
            self.stdout.write('Solving merkato session #%s ...' % ms.pk)
            auctions.solve_session(ms)
            auctions.apply_transfers(ms)
            self.stdout.write('Done')
            flush_cache()
        self.stdout.write('_solve_merkatos completed.')