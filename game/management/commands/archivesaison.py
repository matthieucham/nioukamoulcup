from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import transaction
from game import models as gamemodels
from game.rest import serializers
from ligue1 import models as l1models
import simplejson


class Command(BaseCommand):
    help = 'Fully recompute league instances palmares for finished phases'

    def add_arguments(self, parser):
        parser.add_argument('saison_id', nargs=1, type=int)
        parser.add_argument(
            '--nopalmares',
            action='store_true',
            dest='nopalmares',
            default=False,
            help='Skip palmares computing - be careful'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        saison = l1models.Saison.objects.get(pk=options['saison_id'][0])
        assert (saison.est_la_saison_courante() is False)
        # On s'assure que le palmarès de la saison est sauvegardé avant de détruire les données
        if not options['nopalmares']:
            call_command('makepalmares', saison.pk)
        for instance in gamemodels.LeagueInstance.objects.filter(saison=saison).all():
            gamemodels.LeagueInstancePhase.objects.filter(
                league_instance=instance).delete()  # cascade drop phaseday and teamdayscore
            gamemodels.Signing.objects.filter(league_instance=instance).delete()
            gamemodels.Merkato.objects.filter(league_instance=instance).delete()
            # clear bank history
            gamemodels.BankAccount.objects.filter(team__league=instance.league).delete()
            print('%s of league %s done' % (instance.name, instance.league.name))
        # delete data
        l1models.Journee.objects.filter(saison=saison).delete()
