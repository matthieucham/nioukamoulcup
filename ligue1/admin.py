from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from inline_actions.admin import InlineActionsMixin
from inline_actions.admin import InlineActionsModelAdminMixin

import ligue1
from ligue1 import models
from statnuts import StatnutsClient
from django.conf import settings


class ImportStatnutsSite(admin.AdminSite):
    site_header = "Pilotage de l'import des données depuis Statnuts"


class PerformanceInline(admin.TabularInline):
    model = models.Performance
    can_delete = False
    fields = ('joueur', 'club', 'temps_de_jeu', 'details',)
    readonly_fields = ('joueur', 'club', 'temps_de_jeu', 'details',)
    ordering = ('club',)

    def has_add_permission(self, request):
        return False


class RencontreAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'journee', 'date', 'resultat', 'sn_meeting_uuid', 'derniere_maj']
    list_filter = [('journee', RelatedOnlyFieldListFilter)]
    fields = ('club_domicile', 'club_exterieur', 'date', 'resultat', 'journee', 'sn_meeting_uuid', 'derniere_maj')
    readonly_fields = (
        'club_domicile', 'club_exterieur', 'date', 'resultat', 'journee', 'sn_meeting_uuid', 'derniere_maj')
    ordering = ['date']
    actions = ['import_meetings_action']
    inlines = [PerformanceInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def import_meetings_action(self, request, queryset):
        client = StatnutsClient(settings.STATNUTS_CLIENT_ID, settings.STATNUTS_SECRET, settings.STATNUTS_URL)
        for rencontre in queryset:
            models.Rencontre.objects.import_from_statnuts(rencontre.journee,
                                                          client.get_meeting(rencontre.sn_meeting_uuid),
                                                          client,
                                                          force_import=True)
        self.message_user(request, "Import effectué")
        return HttpResponseRedirect(reverse('import_statnuts:ligue1_rencontre_changelist'))

    import_meetings_action.short_description = "Importer les rencontres sélectionnées"


class RencontreInline(InlineActionsMixin, admin.TabularInline):
    model = models.Rencontre
    can_delete = False
    fields = ('date', 'resultat', 'sn_meeting_uuid', 'derniere_maj',)
    readonly_fields = ('date', 'resultat', 'sn_meeting_uuid', 'derniere_maj',)

    actions = ['import_meeting_action']

    def has_add_permission(self, request):
        return False

    def import_meeting_action(self, request, obj, inline_obj):
        client = StatnutsClient(settings.STATNUTS_CLIENT_ID, settings.STATNUTS_SECRET, settings.STATNUTS_URL)
        models.Rencontre.objects.import_from_statnuts(obj, client.get_meeting(inline_obj.sn_meeting_uuid), client,
                                                      force_import=True)
        messages.info(request, "Import effectué")
        return HttpResponseRedirect(reverse('import_statnuts:ligue1_rencontre_changelist'))

    import_meeting_action.short_description = "Importer ce match"


class JourneeAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ['numero', 'get_saison', 'sn_step_uuid', 'debut', 'fin', 'derniere_maj']
    ordering = ['-saison', '-numero']
    actions = ['import_step_action']
    inlines = [RencontreInline, ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_saison(self, obj):
        return obj.saison.nom

    def import_step_action(self, request, queryset):
        client = StatnutsClient(settings.STATNUTS_CLIENT_ID, settings.STATNUTS_SECRET, settings.STATNUTS_URL)
        for journee in queryset:
            models.Journee.objects.import_from_statnuts(journee.saison, client.get_step(journee.sn_step_uuid), client,
                                                        force_import=True)
        self.message_user(request, "Import effectué")
        return HttpResponseRedirect(reverse('import_statnuts:ligue1_rencontre_changelist'))

    import_step_action.short_description = "Mettre à jour"


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
            models.Saison.objects.import_from_statnuts(client.get_tournament_instance(saison.sn_instance_uuid), client,
                                                       force_import=True)
        self.message_user(request, "Import effectué")
        return HttpResponseRedirect(reverse('import_statnuts:ligue1_journee_changelist'))

    import_instance_action.short_description = "Importer les données de ces saisons"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['sn_tournament'] = ligue1.STATNUTS_TOURNAMENT
        return super(SaisonAdmin, self).changelist_view(request, extra_context=extra_context)


class SaisonCouranteAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin_site = ImportStatnutsSite('import_statnuts')
admin_site.disable_action('delete_selected')
admin_site.register(models.SaisonCourante, SaisonCouranteAdmin)
admin_site.register(models.Saison, SaisonAdmin)
admin_site.register(models.Journee, JourneeAdmin)
admin_site.register(models.Joueur)
admin_site.register(models.Club)
admin_site.register(models.Rencontre, RencontreAdmin)
