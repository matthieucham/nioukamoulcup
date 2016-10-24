from django.contrib import admin

from game import models
from ligue1 import models as l1models
from ligue1.admin import admin_site
from inline_actions.admin import InlineActionsMixin
from inline_actions.admin import InlineActionsModelAdminMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


# Register your models here.
class JourneeScoringInline(InlineActionsMixin, admin.TabularInline):
    model = models.JourneeScoring
    can_delete = False
    fields = ('journee', 'status', 'get_derniere_maj', 'computed_at', 'locked_at',)
    readonly_fields = ('journee', 'status', 'get_derniere_maj', 'computed_at', 'locked_at',)
    actions = ('compute_scores', 'lock',)

    def has_add_permission(self, request):
        return False

    def get_derniere_maj(self, obj):
        return obj.journee.derniere_maj.strftime('%d-%m-%Y %H:%M')

    def compute_scores(self, request, obj, inline_obj):
        inline_obj.save()
        return HttpResponseRedirect(reverse('import_statnuts:game_saisonscoring_change', args=[obj.pk]))

    def lock(self, request, obj, inline_obj):
        inline_obj.lock()
        return HttpResponseRedirect(reverse('import_statnuts:game_saisonscoring_change', args=[obj.pk]))


class SaisonScoringAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ['saison', 'computed_at']
    model = models.SaisonScoring
    actions = ['compute_scores_action']
    inlines = [JourneeScoringInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def compute_scores_action(self, request, queryset):
        for ss in queryset:
            journees = l1models.Journee.objects.filter(saison=ss.saison).order_by('numero')
            # delete all existing journeescorings
            models.JourneeScoring.objects.filter(saison_scoring=ss).delete()
            for journee in journees:
                models.JourneeScoring.objects.create(journee=journee, saison_scoring=ss)
        self.message_user(request, "Calcul effectué")

    compute_scores_action.short_description = "Recalculer les scores"


admin_site.register(models.SaisonScoring, SaisonScoringAdmin)