from rest_framework import serializers
from game.models import league_models


class TeamDayScoreSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField()

    class Meta:
        model = league_models.TeamDayScore
        fields = ('team', 'score', 'attributes')


class LeagueInstancePhaseDaySerializer(serializers.ModelSerializer):
    league_instance_phase = serializers.SlugRelatedField('name', read_only=True)
    results = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('league_instance_phase', 'number', 'results')
