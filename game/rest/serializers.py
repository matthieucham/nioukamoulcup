from rest_framework import serializers
from game.models import league_models


class TeamDayScoreSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(read_only=True)
    team_name = serializers.StringRelatedField(source='team', read_only=True)

    class Meta:
        model = league_models.TeamDayScore
        fields = ('team', 'team_name', 'score', 'attributes')


class LeagueInstancePhaseDaySerializer(serializers.ModelSerializer):
    phase_name = serializers.SlugRelatedField(source='league_instance_phase', slug_field='name', read_only=True)
    results = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('league_instance_phase', 'phase_name', 'number', 'results')
