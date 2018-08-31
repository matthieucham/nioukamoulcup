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
            'apiroot': reverse('api-root', request=request)
        }
        clubs_serializer = serializers.ClubSerializer(
            l1models.Club.objects.filter(participations__est_courante__isnull=False), many=True,
            context={'request': request})
        self.initial_state['clubs'] += self._to_json(clubs_serializer)

    @timed
    def init_from_team(self, request, team):
        self._init_common(request)
        team_serializer = serializers.TeamDetailSerializer(team, context={'request': request})
        players_serializer = serializers.PlayerScoreSerializer(
            l1models.Joueur.objects.filter(signing__team=team), many=True, context={'request': request})
        self.initial_state['team'] = self._to_json(team_serializer)
        self.initial_state['players'] += self._to_json(players_serializer)
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

    # @timed
    # def init_merkatoplayers(self, request, league):
    #     self._init_common(request)
    #     instance = models.LeagueInstance.objects.get_current(league)
    #     user = request.user
    #     team = models.LeagueMembership.objects.filter(user=user, league=league).first().team
    #     qs = (
    #             l1models.Joueur.objects.filter(club__participations=instance.saison) |
    #             l1models.Joueur.objects.filter(performances__rencontre__journee__saison=instance.saison)
    #     ).distinct().order_by('club', 'nom')
    #     base_context = dict({'request': request})
    #     base_context['signings_map'] = dict(models.Signing.objects.filter(team__division=team.division,
    #                                                                       end__isnull=True,
    #                                                                       league_instance=instance).select_related(
    #         'team').values_list('player_id', 'team__name'))
    #     base_context['sales_map'] = dict(
    #         models.Sale.objects.filter(merkato_session__is_solved=False)
    #             .filter(team__division=team.division,
    #                     merkato_session__merkato__league_instance=instance).select_related(
    #             'team').values_list('player_id', 'team__name'))
    #     players_srz = serializers.PlayerMerkatoSerializer(qs, many=True, context=base_context)
    #     self.initial_state.update({'merkatoplayers': self._to_json(players_srz)})
    #     return self.initial_state

    @timed
    def init_from_merkatosession(self, request, session):
        self._init_common(request)
        session_serializer = serializers.MerkatoSessionSerializer(session, context={'request': request})
        self.initial_state.update({'merkatosession': self._to_json(session_serializer)})
        return self.initial_state
