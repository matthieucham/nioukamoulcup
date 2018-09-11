from django.views.generic import DetailView
from rules.contrib.views import PermissionRequiredMixin
from game.models import League, LeagueInstance, LeagueInstancePhase, LeagueInstancePhaseDay, LeagueMembership, Team, \
    MerkatoSession
from game.rest.league import CurrentLeagueInstanceMixin
from game.rest.redux_state import StateInitializerMixin
from game.rest import serializers


class LeagueWallView(PermissionRequiredMixin, StateInitializerMixin, CurrentLeagueInstanceMixin, DetailView):
    model = League
    template_name = 'game/league/wall.html'
    permission_required = 'game.view_league'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueWallView, self).get_context_data(**kwargs)
        league = self.object

        instance = self._get_current_league_instance(league)
        serializer = serializers.LeagueInstancePhaseDaySerializer(
            LeagueInstancePhaseDay.objects.get_latest_day_for_phases(
                LeagueInstancePhase.objects.filter(league_instance=instance)), many=True,
            context={'request': self.request})
        # context['PRELOADED_STATE'] = {
        #     'ranking': []  # json.loads(str(JSONRenderer().render(serializer.data), 'utf-8'))
        # }

        # Get active team from league
        try:
            mb = LeagueMembership.objects.get(user=self.request.user, league=league)
            context['team'] = mb.team
        except LeagueMembership.DoesNotExist:
            pass

        context['component'] = 'test'
        context['instance'] = instance
        context['PRELOADED_STATE'] = self.init_common(self.request, self.object.pk)
        return context


class LeagueEkypView(PermissionRequiredMixin, StateInitializerMixin, CurrentLeagueInstanceMixin, DetailView):
    model = League
    template_name = 'game/league/ekyp.html'
    permission_required = 'game.view_league'

    def _get_my_team(self):
        return LeagueMembership.objects.get(user=self.request.user, league=self.object).team

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueEkypView, self).get_context_data(**kwargs)
        my_team = self._get_my_team()
        context['team'] = my_team
        context['instance'] = self._get_current_league_instance(self.object)

        if 'team_pk' in self.kwargs and self.kwargs['team_pk'] != my_team.pk:
            context['component'] = 'team'
            context['PRELOADED_STATE'] = self.init_from_team(self.request,
                                                             Team.objects.filter(
                                                                 managers__league=self.kwargs['pk']).distinct().get(
                                                                 pk=self.kwargs['team_pk']))
        else:
            context['component'] = 'ekyp'
            context['PRELOADED_STATE'] = self.init_from_team(self.request, my_team)
        return context


class LeagueRankingView(PermissionRequiredMixin, StateInitializerMixin, CurrentLeagueInstanceMixin, DetailView):
    model = League
    template_name = 'game/league/league_base.html'
    permission_required = 'game.view_league'

    def _get_my_team(self):
        return LeagueMembership.objects.get(user=self.request.user, league=self.object).team

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueRankingView, self).get_context_data(**kwargs)
        my_team = self._get_my_team()
        context['team'] = my_team
        context['component'] = 'league'
        context['instance'] = self._get_current_league_instance(self.object)

        context['PRELOADED_STATE'] = self.init_from_league(self.request, self.object)
        return context


class LeagueMerkatoResultsView(PermissionRequiredMixin, StateInitializerMixin, CurrentLeagueInstanceMixin, DetailView):
    model = League
    template_name = 'game/league/merkato_results.html'
    permission_required = 'game.view_league'

    def _get_my_team(self):
        return LeagueMembership.objects.get(user=self.request.user, league=self.object).team

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueMerkatoResultsView, self).get_context_data(**kwargs)
        context['sessions'] = MerkatoSession.objects.filter(
            merkato__league_instance=self._get_current_league_instance(self.object), is_solved=True).order_by(
            '-solving')
        context['team'] = self._get_my_team()
        context['instance'] = self._get_current_league_instance(self.object)
        context['component'] = 'merkato'
        if 'session_pk' in self.kwargs:
            msession = MerkatoSession.objects.get(
                merkato__league_instance=self._get_current_league_instance(self.object), is_solved=True,
                pk=self.kwargs['session_pk'])
            context['PRELOADED_STATE'] = self.init_from_merkatosession(self.request, msession)
        else:
            # latest
            context['PRELOADED_STATE'] = self.init_from_merkatosession(self.request, context['sessions'].first())
        return context
