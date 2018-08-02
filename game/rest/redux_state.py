from rest_framework.reverse import reverse
from . import serializers
from ligue1 import models as l1models
from game import models
from utils.timer import Timer


class StateInitializerMixin:
    """
    Builds the initial states to pass to the front app to populate the redux store.
    Separate entities collected as is from associations between them
    """

    def _to_json(self, serializer):
        # return json.loads(str(JSONRenderer().render(serializer.data), 'utf-8'))
        return serializer.data

    def _init_common(self, request):
        with Timer(id='_init_common', verbose=True):
            self.initial_state = {
                'clubs': list(),
                'players': list(),
                'team': None,
                'apiroot': reverse('api-root', request=request)
            }
            clubs_serializer = serializers.ClubSerializer(
                l1models.Club.objects.filter(participations__est_courante__isnull=False), many=True,
                context={'request': request})
            self.initial_state['clubs'] += self._to_json(clubs_serializer)

    def init_from_team(self, request, team):
        self._init_common(request)
        with Timer(id='init_from_team', verbose=True):
            team_serializer = serializers.TeamDetailSerializer(team, context={'request': request})
            players_serializer = serializers.PlayerScoreSerializer(
                l1models.Joueur.objects.filter(signing__team=team), many=True, context={'request': request})
            self.initial_state['team'] = self._to_json(team_serializer)
            self.initial_state['players'] += self._to_json(players_serializer)
            self.initial_state['league_id'] = team.league.id
            return self.initial_state

    def init_from_league(self, request, league):
        self._init_common(request)
        with Timer(id='init_from_league', verbose=True):
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

    def init_from_merkatosession(self, request, session):
        self._init_common(request)
        with Timer(id='init_from_merkatosession', verbose=True):
            session_serializer = serializers.MerkatoSessionSerializer(session, context={'request': request})
            self.initial_state.update({'merkatosession': self._to_json(session_serializer)})
            return self.initial_state
