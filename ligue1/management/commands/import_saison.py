from django.core.management.base import BaseCommand
from django.db import transaction
from ligue1 import models as l1models
from django.conf import settings
import statnuts


class Command(BaseCommand):
    help = 'Import all data from the saison id'

    def add_arguments(self, parser):
        parser.add_argument('saison_id', nargs='+', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        client = statnuts.StatnutsClient(settings.STATNUTS_CLIENT_ID, settings.STATNUTS_SECRET, settings.STATNUTS_URL,
                                         settings.STATNUTS_NKCUP_USER, settings.STATNUTS_NKCUP_PWD)
        for saison_id in options['saison_id']:
            saison = l1models.Saison.objects.get(pk=saison_id)
            self.stdout.write('Import saison %s ...' % saison.nom)
            l1models.Saison.objects.import_from_statnuts(client.get_tournament_instance(saison.sn_instance_uuid),
                                                         client,
                                                         force_import=True)
            self.stdout.write('Import saison %s terminé' % saison.nom)
