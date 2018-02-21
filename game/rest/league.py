from django.http import Http404
import datetime

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from dry_rest_permissions.generics import DRYObjectPermissions

from game.models import league_models, transfer_models
from ligue1 import models as l1models
from game.rest import serializers


class CurrentLeagueInstanceMixin:
    def _get_current_league_instance(self, pk):
        try:
            return league_models.LeagueInstance.objects.get(league=pk, current=True)
        except league_models.LeagueInstance.DoesNotExist:
            raise Http404


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
        team_pk = self.kwargs['team_pk']
        return league_models.Signing.objects.filter(team=team_pk).order_by('begin')


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

