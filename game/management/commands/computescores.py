from django.core.management.base import BaseCommand, CommandError
from game import models as gamemodels


class Command(BaseCommand):
    help = 'Compute scores from imported results'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Recompute team scores for all journees of the current saison, not just the updated ones'
        )

    def handle(self, *args, **options):
        # prerequisite: statnuts import done
        current_saisonscoring = gamemodels.SaisonScoring.objects.select_related('saison').filter(
            saison__est_courante__isnull=False).first()
        if not current_saisonscoring:
            raise CommandError('No saison marked as current')
        # update JJScores (ponctual scores of players)
        jjs_list = current_saisonscoring.compute()
        if options['force']:
            jjs_list = gamemodels.JourneeScoring.objects.select_related('journee').filter(
                saison_scoring=current_saisonscoring)
        self.stdout.write('%d journees updated to compute' % len(jjs_list))
        # now compute TDS for updated JJS
        licount = 0
        for li in gamemodels.LeagueInstance.objects.filter(saison=current_saisonscoring.saison,
                                                           current=True):  # "current" means the game is still on
            for j in jjs_list:
                self.stdout.write('Computing scores of instance %s for journee %s' % (li.name, j.journee))
                gamemodels.LeagueInstancePhaseDay.objects.compute_results(li, j.journee)
            licount += 1
        self.stdout.write('Done. %d league_instances processed' % licount)