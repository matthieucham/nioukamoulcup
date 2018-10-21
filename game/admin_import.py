from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin
from zinnia_ckeditor.admin import EntryAdminCKEditor

from game import models
from ligue1.admin_import import admin_import_site
from inline_actions.admin import InlineActionsMixin
from inline_actions.admin import InlineActionsModelAdminMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from game.services import auctions


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

    def compute_scores(self, request, obj, parent_obj):
        obj.save()
        return HttpResponseRedirect(reverse('import_statnuts:game_saisonscoring_change', args=[parent_obj.pk]))

    def lock(self, request, obj, parent_obj):
        obj.lock()
        return HttpResponseRedirect(reverse('import_statnuts:game_saisonscoring_change', args=[parent_obj.pk]))


class SaisonScoringAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    list_display = ['saison', 'computed_at']
    model = models.SaisonScoring
    actions = ['compute_scores_action', 'archive_saison_action']
    inlines = [JourneeScoringInline]

    def has_delete_permission(self, request, obj=None):
        return False

    def compute_scores_action(self, request, queryset):
        for ss in queryset:
            ss.compute()
        self.message_user(request, "Calcul effectué")

    def archive_saison_action(self, request, queryset):
        for ss in queryset:
            ss.archive()
        self.message_user(request, "Saison archivée")

    compute_scores_action.short_description = "Recalculer les scores"
    archive_saison_action.short_description = "Archiver"


class MerkatoSessionInline(admin.TabularInline):
    model = models.MerkatoSession
    fields = ['closing', 'solving', 'is_solved', 'attributes']
    can_delete = False
    extra = 0


class DraftSessionRankInline(admin.TabularInline):
    model = models.DraftSessionRank
    fields = ['team', 'rank']


class DraftSessionAdmin(admin.ModelAdmin):
    model = models.DraftSession
    list_display = ['merkato', 'number', 'closing', 'is_solved']
    inlines = [DraftSessionRankInline, ]
    actions = ['solve_draft_action', ]

    def solve_draft_action(self, request, queryset):
        for ds in queryset:
            if ds.closing > timezone.now():
                self.message_user(request, "C'est trop tôt !",
                                  level=messages.ERROR)
            else:
                auctions.solve_draft_session(ds)
        return HttpResponseRedirect(reverse('import_statnuts:game_draftsession_changelist'))


class MerkatoAdmin(admin.ModelAdmin):
    model = models.Merkato
    list_display = ['begin', 'end', 'mode']
    actions = ['generate_sessions_action', 'init_accounts_action']
    inlines = [MerkatoSessionInline, ]

    def has_delete_permission(self, request, obj=None):
        return True

    def generate_sessions_action(self, request, queryset):
        for m in queryset:
            if m.begin < timezone.now():
                self.message_user(request, "Le merkato %s ayant démarré, impossible de modifier ses sessions" % m,
                                  level=messages.ERROR)
            else:
                models.MerkatoSession.objects.filter(merkato=m).delete()
                models.Merkato.objects.create_sessions(m)
        self.message_user(request, "Sessions créées")
        return HttpResponseRedirect(reverse('import_statnuts:game_merkato_changelist'))

    def init_accounts_action(self, request, queryset):
        for m in queryset.filter(mode='BID'):
            if 'init_balance' in m.configuration:
                for team in models.Team.objects.filter(league=m.league_instance.league):
                    models.BankAccount.objects.init_account(m.begin.date(), team, m.configuration.get('init_balance'),
                                                            m)
        return HttpResponseRedirect(reverse('import_statnuts:game_merkato_changelist'))


admin_import_site.register(models.SaisonScoring, SaisonScoringAdmin)
admin_import_site.register(models.Merkato, MerkatoAdmin)
admin_import_site.register(models.DraftSession, DraftSessionAdmin)


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


class LeagueDivisionInline(admin.TabularInline):
    model = models.LeagueDivision
    extra = 0


class LeagueInvitationInline(InlineActionsMixin, admin.TabularInline):
    model = models.LeagueInvitation
    readonly_fields = ('team', 'status',)

    def get_inline_actions(self, request, obj=None):
        actions = super(LeagueInvitationInline, self).get_inline_actions(request, obj)
        if obj:
            if obj.status == 'OPENED':
                actions.extend(('accept', 'reject'))
        return actions

    def has_add_permission(self, request):
        return False

    def accept(self, request, obj, parent_obj):
        obj.accept()
        return HttpResponseRedirect(reverse('import_statnuts:game_league_change', args=[parent_obj.pk]))

    def reject(self, request, obj, parent_obj):
        obj.reject()
        return HttpResponseRedirect(reverse('import_statnuts:game_league_change', args=[parent_obj.pk]))


class TeamInline(admin.TabularInline):
    model = models.Team
    extra = 0
    fields = ('name', 'attributes', 'division')
    can_delete = False

    def has_add_permission(self, request):
        return False


class LeagueAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    model = models.League
    readonly_fields = ('code',)
    inlines = [LeagueDivisionInline, TeamInline, LeagueInvitationInline, ]


class TeamAdmin(admin.ModelAdmin):
    model = models.Team
    list_display = ('name', 'league', 'division', 'get_managers_names')


admin.site.register(Entry, EntryLeagueAdmin)
admin_import_site.register(models.League, LeagueAdmin)
admin_import_site.register(models.LeagueInstance)
admin_import_site.register(models.LeagueInstancePhase)
admin_import_site.register(models.Team, TeamAdmin)
