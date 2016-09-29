from django.contrib import admin

import ligue1
from ligue1 import models
from statnuts import StatnutsClient
from nioukamoulcup import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class ImportStatnutsSite(admin.AdminSite):
    site_header = "Pilotage de l'import des données depuis Statnuts"


class JourneeAdmin(admin.ModelAdmin):
    list_display = ['numero', 'get_saison', 'sn_step_uuid', 'debut', 'fin', 'derniere_maj']
    ordering = ['-saison', '-numero']
    actions = ['import_step_action']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_saison(self, obj):
        return obj.saison.nom

    def import_step_action(self, request, queryset):
        pass

    import_step_action.short_description = "Importer les données de ces journées"


class SaisonAdmin(admin.ModelAdmin):
    actions = ['import_instance_action', 'delete_selected']
    list_display = ['nom', 'sn_instance_uuid', 'debut', 'fin', 'derniere_maj']

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return obj.journees.count() == 0
        return False

    def import_instance_action(self, request, queryset):
        # appeler Statnuts ici
        client = StatnutsClient(settings.STATNUTS_CLIENT_ID, settings.STATNUTS_SECRET, settings.STATNUTS_URL)
        for saison in queryset:
            saison.import_from_statnuts(client.get_tournament_instance(saison.sn_instance_uuid), client)
        self.message_user(request, "Import effectué")
        return HttpResponseRedirect(reverse('import_statnuts:ligue1_journee_changelist'))

    import_instance_action.short_description = "Importer les données de ces saisons"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['sn_tournament'] = ligue1.STATNUTS_TOURNAMENT
        return super(SaisonAdmin, self).changelist_view(request, extra_context=extra_context)


admin_site = ImportStatnutsSite('import_statnuts')
admin_site.disable_action('delete_selected')
admin_site.register(models.Saison, SaisonAdmin)
admin_site.register(models.Journee, JourneeAdmin)
admin_site.register(models.Joueur)
admin_site.register(models.Club)
