from rest_framework.reverse import reverse
from . import serializers
from ligue1 import models as l1models
from game import models
from utils.timer import timed


class StateInitializerMixin:
    """
    Builds the initial states to pass to the front app to populate the redux store.
    Separate entities collected as is from associations between them
    """

    @timed
    def _to_json(self, serializer):
        # return json.loads(str(JSONRenderer().render(serializer.data), 'utf-8'))
        return serializer.data

    @timed
    def _init_common(self, request):
        self.initial_state = {
            'clubs': list(),
            'players': list(),
            'team': None,
            'apiroot': reverse('api-root', request=request),
        }
        clubs_serializer = serializers.ClubSerializer(
            l1models.Club.objects.filter(participations__est_courante__isnull=False), many=True,
            context={'request': request})
        self.initial_state['clubs'] += self._to_json(clubs_serializer)

    @timed
    def init_common(self, request, league_id=None):
        self._init_common(request)
        self.initial_state.update({'league_id': league_id})
        return self.initial_state

    @timed
    def init_from_team(self, request, team):
        self._init_common(request)
        team_serializer = serializers.TeamDetailSerializer(team, context={'request': request,
                                                                          'current': True})  # TODO optim pour FSY
        players_serializer = serializers.PlayerScoreSerializer(
            l1models.Joueur.objects.filter(signing__team=team), many=True, context={'request': request})
        palmares_serializer = serializers.TeamPalmaresSerializer(
            models.TeamPalmaresRanking.objects.filter(team=team).filter(rank__lt=4).order_by(
                '-palmares__league_instance_end'), many=True
        )
        self.initial_state['team'] = self._to_json(team_serializer)
        self.initial_state['players'] += self._to_json(players_serializer)
        self.initial_state['palmares'] = self._to_json(palmares_serializer)
        self.initial_state['league_id'] = team.league.id
        return self.initial_state

    @timed
    def init_from_league(self, request, league):
        self._init_common(request)
        ranking_serializer = serializers.LeagueInstanceRankingSerializer(
            models.LeagueInstance.objects.get(league=league, current=True), context={'request': request})
        teaminfo_serializer = serializers.TeamInfoSerializer(
            models.Team.objects.select_related('bank_account').select_related('division').filter(league=league),
            many=True,
            context={'request': request})
        self.initial_state.update({'ranking': self._to_json(ranking_serializer)})
        self.initial_state.update({'teams': self._to_json(teaminfo_serializer)})
        self.initial_state.update({'league_id': league.id})
        return self.initial_state

    @timed
    def init_from_merkatosession(self, request, session):
        self._init_common(request)
        session_serializer = serializers.MerkatoSessionSerializer(session, context={'request': request})
        self.initial_state.update({'merkatosession': self._to_json(session_serializer)})
        return self.initial_state

    @timed
    def init_from_draftsession(self, request, session):
        self._init_common(request)
        session_serializer = serializers.DraftSessionSerializer(session, context={'request': request})
        self.initial_state.update({'draftsession': self._to_json(session_serializer)})
        return self.initial_state

    @timed
    def init_current_merkatos(self, request, team, merkatos):
        self._init_common(request)
        self.initial_state.update({'league_id': team.league.pk})
        merkato_serializer = serializers.CurrentMerkatoSerializer(merkatos, many=True,
                                                                  context={'request': request, 'team': team})
        team_serializer = serializers.TeamDetailSerializer(team, context={'request': request,
                                                                          'current': True})
        self.initial_state.update({'merkatos': self._to_json(merkato_serializer)})
        self.initial_state.update({'team': self._to_json(team_serializer)})
        return self.initial_state

    @timed
    def init_from_palmares(self, request, league, palmares_pk=None):
        self._init_common(request)
        if palmares_pk:
            palmares_serializer = serializers.PalmaresSerializer(
                models.Palmares.objects.filter(league=league).get(pk=palmares_pk), context={'request': request})
        else:
            palmares_serializer = serializers.PalmaresSerializer(
                models.Palmares.objects.filter(league=league).order_by('-league_instance_end').first(),
                context={'request': request})
        self.initial_state.update({'palmares': self._to_json(palmares_serializer)})
        self.initial_state.update({'league_id': league.id})
        return self.initial_state
