from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin
from zinnia_ckeditor.admin import EntryAdminCKEditor

from game import models
from ligue1.admin import admin_site
from inline_actions.admin import InlineActionsMixin
from inline_actions.admin import InlineActionsModelAdminMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


# Register your models here.
class JourneeScoringInline(InlineActionsMixin, admin.TabularInline):
    model = models.JourneeScoring
    can_delete = False
    fields = ('journee', 'status', 'get_derniere_maj', 'computed_at', 'locked_at',)
    readonly_fields = ('journee', 'status', 'get_derniere_maj', 'computed_at', 'locked_at',)
    inline_actions = ('compute_scores', 'lock',)

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

    def has_delete_permission(self, request, obj=None):
        return False

    def compute_scores_action(self, request, queryset):
        for ss in queryset:
            ss.compute()
        self.message_user(request, "Calcul effectué")

    compute_scores_action.short_description = "Recalculer les scores"


admin_site.register(models.SaisonScoring, SaisonScoringAdmin)


class EntryLeagueAdmin(EntryAdminCKEditor):
    # In our case we put the gallery field
    # into the 'Content' fieldset
    fieldsets = (
                    (_('Content'), {
                        'fields': (('title', 'status'), 'lead', 'content', 'league')}),
                ) + \
                EntryAdmin.fieldsets[1:]
    readonly_fields = (
        'league',
    )

    def save_model(self, request, obj, form, change):
        # TODO : pass a param to know if league entry / info entry : param set on the template ?
        visited_league_pk = request.session.get('visited_league', None)
        if visited_league_pk:
            obj.league = models.LeagueMembership.objects.filter(user=request.user).get(league=visited_league_pk).league
        else:
            obj.league = None
        super().save_model(request, obj, form, change)


admin.site.register(Entry, EntryLeagueAdmin)
