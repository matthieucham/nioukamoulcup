from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from game.models import league_models
from game.rest import serializers


class LeagueInstanceRankingView(APIView):
    def _get_current_league_instance(self, pk):
        try:
            return league_models.LeagueInstance.objects.get(league=pk, current=True)
        except league_models.LeagueInstance.DoesNotExist:
            raise Http404

    def get(self, request, league_pk, format=None):
        instance = self._get_current_league_instance(league_pk)
        # TODO : check membership user / league via django rules
        latest_days = []
        for ph in league_models.LeagueInstancePhase.objects.filter(league_instance=instance):
            latest_day = league_models.LeagueInstancePhaseDay.objects.filter(league_instance_phase=ph,
                                                                             results__isnull=False).prefetch_related(
                'teamdayscore_set').order_by('-number').first()
            if latest_day:
                latest_days.append(latest_day)
        serializer = serializers.LeagueInstancePhaseDaySerializer(latest_days, many=True)
        return Response(serializer.data)

