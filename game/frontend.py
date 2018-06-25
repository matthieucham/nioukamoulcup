from django.views.generic import TemplateView, DetailView
from django.db.models import Sum, Avg, Count, Q
from graphos.sources.model import SimpleDataSource
from graphos.renderers.morris import AreaChart
# from graphos.renderers.gchart import AreaChart
from rules.contrib.views import PermissionRequiredMixin
from rest_framework.renderers import JSONRenderer
import json

from . import models
from ligue1 import models as l1models
from .rest.league import CurrentLeagueInstanceMixin
from .rest.redux_state import StateInitializerMixin
from .rest import serializers
from .services.scoring import BONUS


class HomePage(TemplateView):
    template_name = 'game/home/info.html'


class ResultRencontreView(DetailView):
    model = l1models.Rencontre
    template_name = 'game/home/result_rencontre.html'


class ClubView(DetailView):
    model = l1models.Club
    template_name = 'game/home/club_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClubView, self).get_context_data(**kwargs)
        saisonscoring = models.SaisonScoring.objects.filter(saison__est_courante__isnull=False).first()
        context['players'] = []
        for j in self.object.joueurs.prefetch_related('jjscore_set').annotate(
                nb_notes=Count('jjscore', filter=Q(jjscore__journee_scoring__saison_scoring=saisonscoring,
                                                   jjscore__note__isnull=False))):
            context['players'].append(j)
        # for pos in ['G', 'D', 'M', 'A']:
        #     context[pos] = self.object.joueurs.filter(poste=pos).order_by('nom')
        return context


class StatJoueurView(DetailView):
    model = l1models.Joueur
    template_name = 'game/home/stat_joueur.html'

    def _compute_stats_agg(self, jjscores):
        agg = dict()
        for bk in set(BONUS['COLLECTIVE'].keys()).union(set(BONUS['PERSONAL'].keys())):
            agg[bk] = 0
        for jjs in jjscores:
            for bk in set(BONUS['COLLECTIVE'].keys()).union(set(BONUS['PERSONAL'].keys())):
                if 'bonuses' in jjs.details and bk in jjs.details['bonuses']:
                    agg[bk] += jjs.details['bonuses'][bk]
        agg['AVGNOTE'] = round(jjscores.filter(note__isnull=False).aggregate(Avg('note'))['note__avg'] or 0, 2)
        agg['NBNOTE'] = jjscores.filter(note__isnull=False).count()
        agg['BONUS'] = jjscores.aggregate(Sum('bonus'))['bonus__sum'] or 0
        return agg

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StatJoueurView, self).get_context_data(**kwargs)
        # Step 1: Create a DataPool with the data we want to retrieve.
        saisonscoring = models.SaisonScoring.objects.filter(saison__est_courante__isnull=False).first()
        jjscores = models.JJScore.objects.list_scores_for_joueur(joueur=self.object,
                                                                 saison_scoring=saisonscoring) \
            .select_related('rencontre__club_domicile') \
            .select_related('rencontre__club_exterieur').select_related('journee_scoring__journee')
        context['stats'] = self._compute_stats_agg(jjscores)
        context['jjscores'] = jjscores
        data_source_array = [['J', 'Note', 'Bonus']]
        for jjs in jjscores:
            data_source_array.append([jjs.journee_scoring.journee.numero,
                                      round(float(jjs.note or 0) + float(jjs.compensation or 0), 3),
                                      float(jjs.bonus or 0)])
        data_source = SimpleDataSource(data_source_array)
        context['chart'] = AreaChart(data_source,
                                     # width=580,
                                     options={'resize': True,
                                              'hideHover': 'auto',
                                              'parseTime': False,
                                              'fillOpacity': 0.6,
                                              'ymin': 0,
                                              'ymax': 'auto 15',
                                              'grid': False,
                                              'behaveLikeLine': False,
                                              'goals': [0.0, 5.0, 10.0, 15.0, 20.0, 25.0]}
                                     # options={
                                     #     'title': self.object.display_name(),
                                     #     'isStacked': True,
                                     #     'legend': {'position': 'top', 'maxLines': 3},
                                     #     'hAxis': {'title': 'Journée'},
                                     #     'vAxis': {'title': 'Points', 'minValue': 0, 'ticks': [5, 10, 15, 20]},
                                     #     'chartArea': {'left': 'auto', 'top': 'auto', 'width': '80%', 'height': '80%'},
                                     #     'crosshair': {'trigger': 'both'},
                                     #     'curveType': 'function',
                                     #     'focusTarget': 'category',
                                     #     'pointSize': 5,
                                     # }
                                     )
        return context


class LeagueWallView(PermissionRequiredMixin, CurrentLeagueInstanceMixin, DetailView):
    model = models.League
    template_name = 'game/league/wall.html'
    permission_required = 'game.view_league'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueWallView, self).get_context_data(**kwargs)
        league = self.object

        instance = self._get_current_league_instance(league)
        serializer = serializers.LeagueInstancePhaseDaySerializer(
            models.LeagueInstancePhaseDay.objects.get_latest_day_for_phases(
                models.LeagueInstancePhase.objects.filter(league_instance=instance)), many=True,
            context={'request': self.request})
        context['PRELOADED_STATE'] = {
            'ranking': json.loads(str(JSONRenderer().render(serializer.data), 'utf-8'))
        }

        # Get active team from league
        try:
            mb = models.LeagueMembership.objects.get(user=self.request.user, league=league)
            context['team'] = mb.team
        except models.LeagueMembership.DoesNotExist:
            pass

        context['component'] = 'test'
        context['instance'] = instance
        return context


class LeagueEkypView(PermissionRequiredMixin, StateInitializerMixin, CurrentLeagueInstanceMixin, DetailView):
    model = models.League
    template_name = 'game/league/ekyp.html'
    permission_required = 'game.view_league'

    def _get_my_team(self):
        return models.LeagueMembership.objects.get(user=self.request.user, league=self.object).team

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueEkypView, self).get_context_data(**kwargs)
        my_team = self._get_my_team()
        context['team'] = my_team
        context['instance'] = self._get_current_league_instance(self.object)

        if 'team_pk' in self.kwargs and self.kwargs['team_pk'] != my_team.pk:
            context['component'] = 'team'
            context['PRELOADED_STATE'] = self.init_from_team(self.request,
                                                             models.Team.objects.filter(
                                                                 managers__league=self.kwargs['pk']).distinct().get(
                                                                 pk=self.kwargs['team_pk']))
        else:
            context['component'] = 'ekyp'
            context['PRELOADED_STATE'] = self.init_from_team(self.request, my_team)
        return context


class LeagueRankingView(PermissionRequiredMixin, StateInitializerMixin, CurrentLeagueInstanceMixin, DetailView):
    model = models.League
    template_name = 'game/league/league_base.html'
    permission_required = 'game.view_league'

    def _get_my_team(self):
        return models.LeagueMembership.objects.get(user=self.request.user, league=self.object).team

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueRankingView, self).get_context_data(**kwargs)
        my_team = self._get_my_team()
        context['team'] = my_team
        context['component'] = 'league'
        context['instance'] = self._get_current_league_instance(self.object)

        context['PRELOADED_STATE'] = self.init_from_league(self.request, self.object)
        return context
