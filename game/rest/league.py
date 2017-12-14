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


class LeagueInstanceRankingView(CurrentLeagueInstanceMixin, APIView):
    permission_classes = (DRYObjectPermissions,)

    def get(self, request, league_pk, format=None):
        instance = self._get_current_league_instance(league_pk)
        serializer = serializers.LeagueInstancePhaseDaySerializer(
            league_models.LeagueInstancePhaseDay.objects.get_latest_day_for_phases(
                league_models.LeagueInstancePhase.objects.filter(league_instance=instance)),
            many=True,
            context={'request': request})
        return Response(serializer.data)


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
        return transfer_models.Sale.objects.get_for_team(team_pk)


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
