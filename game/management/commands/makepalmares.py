from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from game import models as gamemodels
from game.rest import serializers
from ligue1 import models as l1models


class Command(BaseCommand):
    help = 'Fully recompute league instances palmares for finished phases'

    def add_arguments(self, parser):
        parser.add_argument('saison_id', nargs=1, type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            saison = l1models.Saison.objects.get(pk=options['saison_id'][0])
        except l1models.Saison.DoesNotExist:
            raise CommandError('Saison %s does not exist' % options['saison_id'][0])
        for instance in gamemodels.LeagueInstance.objects.filter(saison=saison):
            store_phases = []
            for ph in gamemodels.LeagueInstancePhase.objects.filter(league_instance=instance):
                ph_rest = serializers.PhaseRankingSerializer(
                    context={'expand_attributes': True, 'request': None}).to_representation(ph)
                if ph_rest["current_ranking"]["number"] == ph_rest["journee_last"]:
                    store_phases.append((ph.pk, ph_rest))
            for phid, phranking in store_phases:
                pass
