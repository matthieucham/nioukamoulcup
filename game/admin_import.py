from django.contrib import admin

from game import models
from ligue1 import models as l1models
from ligue1.admin_import import admin_import_site
from inline_actions.admin import InlineActionsMixin
from inline_actions.admin import InlineActionsModelAdminMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages


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


class MerkatoSessionInline(admin.TabularInline):
    model = models.MerkatoSession
    fields = ['closing', 'solving', 'is_solved', 'attributes']
    can_delete = False
    extra = 0


class MerkatoAdmin(admin.ModelAdmin):
    model = models.Merkato
    list_display = ['begin', 'end', 'mode']
    actions = ['generate_sessions_action']
    inlines = [MerkatoSessionInline, ]

    def has_delete_permission(self, request, obj=None):
        return True

    def generate_sessions_action(self, request, queryset):
        for m in queryset:
            if m.begin < timezone.now():
                self.message_user(request, "Le merkato %s ayant déjà démarré, impossible de modifier ses sessions" % m,
                                  level=messages.ERROR)
            else:
                models.MerkatoSession.objects.filter(merkato=m).delete()
                models.Merkato.objects.create_sessions(m)
        self.message_user(request, "Sessions créées")
        return HttpResponseRedirect(reverse('import_statnuts:game_merkato_changelist'))


admin_import_site.register(models.SaisonScoring, SaisonScoringAdmin)
admin_import_site.register(models.Merkato, MerkatoAdmin)