from rest_framework import serializers
from django.db import models
from game.models import league_models
import json


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = league_models.Team
        fields = ('id', 'name')


class TeamDayScoreByDivisionSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        """
        List of instances (teamdayscore) -> grouped by team.division
        """
        iterable = instance.all() if isinstance(instance, models.Manager) else instance
        if not iterable:
            return super().to_representation(instance)
        one_tds = iterable[0]
        for div in league_models.LeagueDivision.objects.filter(
                league=one_tds.day.league_instance_phase.league_instance.league):
            div_ranking = super().to_representation(
                league_models.TeamDayScore.objects.filter(day=one_tds.day, team__division=div).order_by('-score'))
            yield {div.name: div_ranking}


class TeamDayScoreSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    is_complete = serializers.SerializerMethodField()

    def get_is_complete(self, obj):
        """
        Check if team roster is complete
        """
        attrs = json.loads(obj.attributes)
        # for each position in 'formation', check if there is enough players in 'composition'
        for pos, req_nb in attrs['formation'].items():
            if len(attrs['composition'][pos]) < req_nb:
                return False
        return True

    class Meta:
        model = league_models.TeamDayScore
        fields = ('team', 'score', 'is_complete')
        list_serializer_class = TeamDayScoreByDivisionSerializer


class LeagueInstancePhaseDaySerializer(serializers.ModelSerializer):
    phase_name = serializers.SlugRelatedField(source='league_instance_phase', slug_field='name', read_only=True)
    results = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('league_instance_phase', 'phase_name', 'number', 'results')
