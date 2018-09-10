from django.http import Http404
from django.utils.timezone import localtime, now

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

from dry_rest_permissions.generics import DRYObjectPermissions

from game.models import league_models, transfer_models
from ligue1 import models as l1models
from game.rest import serializers
from utils.timer import timed


class CurrentLeagueInstanceMixin:
    def _get_current_league_instance(self, pk):
        return league_models.LeagueInstance.objects.get_current(league=pk)


class LeagueInstanceRankingView(generics.RetrieveAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.LeagueInstanceRankingSerializer

    def get_queryset(self):
        return league_models.LeagueInstance.objects.filter(current=True)


class TeamDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.TeamDetailSerializer
    queryset = league_models.Team.objects.all()
    permission_classes = (DRYObjectPermissions,)

    def get_serializer_context(self):
        return {'request': self.request}


class ClubListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    serializer_class = serializers.ClubSerializer

    def get_queryset(self):
        league_pk = self.kwargs['league_pk']
        instance = self._get_current_league_instance(league_pk)
        return l1models.Club.objects.filter(participations=instance.saison)


class TeamSigningsListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.SigningSerializer
    ordering_fields = ('begin',)
    ordering = ('begin',)

    def get_queryset(self):
        team = league_models.Team.objects.get(pk=self.kwargs['team_pk'])
        return league_models.Signing.objects.filter(team=team, league_instance=self._get_current_league_instance(
            team.league)).order_by('begin')


class TeamBankAccountHistoryListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.BankAccountHistorySerializer
    ordering_fields = ('date',)
    ordering = ('date',)

    def get_queryset(self):
        team_pk = self.kwargs['team_pk']
        return league_models.BankAccountHistory.objects.filter(bank_account__team=team_pk)


class TeamReleasesListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.ReleaseSerializer

    def get_queryset(self):
        team_pk = self.kwargs['team_pk']
        return transfer_models.Release.objects.get_for_team(team_pk)


class TeamSalesListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.SaleSerializer

    def get_queryset(self):
        team_pk = self.kwargs['team_pk']
        return transfer_models.Sale.objects.get_for_team(league_models.Team.objects.get(pk=team_pk))


class LeagueResultsByJourneeListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.TeamDayScoreSerializer

    def get_queryset(self):
        team_pk = self.kwargs['team_pk']
        league_pk = self.kwargs['league_pk']
        journee_numero = self.kwargs['journee_numero']

        days = league_models.LeagueInstancePhaseDay.objects.filter(
            league_instance_phase__league_instance=self._get_current_league_instance(league_pk),
            journee__numero=journee_numero
        )
        return league_models.TeamDayScore.objects.filter(day__in=days, team=team_pk).order_by(
            'day__league_instance_phase')


class LeaguePlayersRankingView(CurrentLeagueInstanceMixin, generics.RetrieveAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.PlayersRankingSerializer
    lookup_field = 'league'

    def get_queryset(self):
        league = self.kwargs['league']
        return league_models.LeagueInstance.objects.filter(league=league, current=True)


class LeagueTeamInfoListView(generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.TeamInfoSerializer

    def get_queryset(self):
        league_pk = self.kwargs['pk']
        qs = league_models.Team.objects.filter(league=league_pk)
        qs = self.get_serializer_class().setup_eager_loading(qs)
        return qs


class LeagueMerkatosListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.MerkatoSerializer

    def get_queryset(self):
        return transfer_models.Merkato.objects.filter(
            league_instance=self._get_current_league_instance(self.kwargs['league_pk'])).order_by('begin')


class MerkatoSessionView(CurrentLeagueInstanceMixin, generics.RetrieveAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.MerkatoSessionSerializer
    queryset = transfer_models.MerkatoSession.objects.filter(is_solved=True)


class PlayersForMerkatoView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.PlayerMerkatoSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filter_fields = {
        'poste': ['exact'],
        'club': ['exact', 'isnull']
    }
    search_fields = ('nom', 'surnom', '=prenom',)

    @timed
    def get_queryset(self):
        # limit to players which :
        # - are members of participating teams of the season of the current instance
        # - or have played at least one meeting in the season of the current instance
        # order by club then name
        instance = self._get_current_league_instance(self.kwargs['league_pk'])
        qs = (
                l1models.Joueur.objects.filter(club__participations=instance.saison) |
                l1models.Joueur.objects.filter(performances__rencontre__journee__saison=instance.saison)
        ).distinct().order_by('club__nom', 'nom')
        return qs

    @timed
    def get_serializer_context(self):
        base_context = super(PlayersForMerkatoView, self).get_serializer_context()
        league_pk = self.kwargs['league_pk']
        user = base_context.get('request').user
        team = league_models.LeagueMembership.objects.filter(user=user, league=league_pk).first().team
        base_context['signings_map'] = dict(league_models.Signing.objects.filter(team__division=team.division,
                                                                                 end__isnull=True,
                                                                                 league_instance=self._get_current_league_instance(
                                                                                     league_pk)).select_related(
            'team').values_list('player_id', 'team__name'))
        base_context['sales_map'] = dict(
            transfer_models.Sale.objects.filter(merkato_session__is_solved=False)
                .filter(team__division=team.division,
                        merkato_session__merkato__league_instance=self._get_current_league_instance(
                            league_pk)).select_related(
                'team').values_list('player_id', 'team__name'))
        return base_context


class CurrentMerkatoView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.CurrentMerkatoSerializer

    def get_queryset(self):
        instance = self._get_current_league_instance(self.kwargs['league_pk'])
        return transfer_models.Merkato.objects.filter(league_instance=instance, end__gt=localtime(now())).order_by(
            'begin')
