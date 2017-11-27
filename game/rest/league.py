from django.http import Http404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from dry_rest_permissions.generics import DRYObjectPermissions

from game.models import league_models
from ligue1 import models as l1models
from game.rest import serializers


class CurrentLeagueInstanceMixin():
    def _get_current_league_instance(self, pk):
        try:
            return league_models.LeagueInstance.objects.get(league=pk, current=True)
        except league_models.LeagueInstance.DoesNotExist:
            raise Http404


class LeagueInstanceRankingView(CurrentLeagueInstanceMixin, APIView):
    permission_classes = (DRYObjectPermissions, )

    def get(self, request, league_pk, format=None):
        instance = self._get_current_league_instance(league_pk)
        serializer = serializers.LeagueInstancePhaseDaySerializer(
            league_models.LeagueInstancePhaseDay.objects.get_latest_day_for_phases(
                league_models.LeagueInstancePhase.objects.filter(league_instance=instance)), many=True)
        return Response(serializer.data)


class TeamDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.TeamDetailSerializer
    queryset = league_models.Team.objects.all()
    permission_classes = (DRYObjectPermissions, )

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

    def get_queryset(self):
        team_pk = self.kwargs['team_pk']
        return league_models.Signing.objects.filter(team=team_pk).order_by('begin')

