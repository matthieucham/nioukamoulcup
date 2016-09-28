from django.contrib import admin

import ligue1
from ligue1 import models
from statnuts import StatnutsClient
from nioukamoulcup import settings
import datetime


class ImportStatnutsSite(admin.AdminSite):
    site_header = "Pilotage de l'import des données depuis Statnuts"


class JourneeAdmin(admin.ModelAdmin):
    list_display = ['get_saison', 'numero', 'sn_step_uuid', 'debut', 'fin', 'derniere_maj']

    def has_add_permission(self, request):
        return False

    def get_saison(self, obj):
        return obj.saison.nom


class SaisonAdmin(admin.ModelAdmin):
    actions = ['import_saison_action']
    list_display = ['nom', 'sn_instance_uuid', 'debut', 'fin', 'derniere_maj']

    def import_saison_action(self, request, queryset):
        # appeler Statnuts ici
        client = StatnutsClient(settings.STATNUTS_CLIENT_ID, settings.STATNUTS_SECRET, settings.STATNUTS_URL)
        for saison in queryset:
            journees = client.get_journees(saison.sn_instance_uuid)
            for step in journees['steps']:
                renc = client.get_rencontres(step['uuid'])
                debut, fin = datetime.date(datetime.MAXYEAR, 1, 1), datetime.date(datetime.MINYEAR, 1, 1)
                for x in (rencontre['date'] for rencontre in renc['meetings']):
                    debut, fin = min(x, debut), max(x, fin)
                defaults = {'numero': int(step['name']), 'debut': debut, 'fin': fin}
                models.Journee.objects.get_or_create(
                    sn_step_uuid=step['uuid'],
                    saison=saison,
                    defaults=defaults
                )
            saison.save()
        self.message_user(request, "Import effectué")

    import_saison_action.short_description = "Importer les données de ces saisons"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['sn_tournament'] = ligue1.STATNUTS_TOURNAMENT
        return super(SaisonAdmin, self).changelist_view(request, extra_context=extra_context)


admin_site = ImportStatnutsSite('import_statnuts')
admin_site.register(models.Saison, SaisonAdmin)
admin_site.register(models.Journee, JourneeAdmin)
