from django.contrib import admin

import ligue1
from ligue1 import models


class ImportStatnutsSite(admin.AdminSite):
    site_header = "Pilotage de l'import des données depuis Statnuts"


class SaisonAdmin(admin.ModelAdmin):

    actions = ['import_saison_action']
    list_display = ['nom', 'sn_instance_uuid', 'debut', 'fin', 'derniere_maj']

    def import_saison_action(self, request, queryset):
        # appeler Statnuts ici
        for saison in queryset:
            saison.save()
        self.message_user(request, "Import effectué")
    import_saison_action.short_description = "Importer les données de ces saisons"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['sn_tournament'] = ligue1.STATNUTS_TOURNAMENT
        return super(SaisonAdmin, self).changelist_view(request, extra_context=extra_context)

admin_site = ImportStatnutsSite('import_statnuts')
admin_site.register(models.Saison, SaisonAdmin)
admin_site.register(models.Journee)
