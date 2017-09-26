from rest_framework import serializers
from django.db import models
import json

from game.models import league_models
from ligue1 import models as l1models


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = l1models.Club
        fields = ('id', 'nom', 'maillot_svg', 'maillot_color_bg', 'maillot_color1', 'maillot_color2')


class ClubHdrSerializer(serializers.ModelSerializer):
    class Meta:
        model = l1models.Club
        fields = ('id', 'nom')


class PlayerHdrSerializer(serializers.ModelSerializer):
    club = ClubHdrSerializer()

    class Meta:
        model = l1models.Joueur
        fields = ('id', 'prenom', 'nom', 'surnom', 'poste', 'club')


class TeamHdrSerializer(serializers.ModelSerializer):
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
                league=one_tds.day.league_instance_phase.league_instance.league).order_by('upper_division'):
            div_ranking = super().to_representation(
                league_models.TeamDayScore.objects.filter(day=one_tds.day, team__division=div).order_by('-score'))
            yield {'id': div.id, 'name': div.name, 'ranking': div_ranking}


class TeamDayScoreSerializer(serializers.ModelSerializer):
    team = TeamHdrSerializer(read_only=True)
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


class SigningSerializer(serializers.ModelSerializer):
    player = PlayerHdrSerializer()
    team = TeamHdrSerializer()

    class Meta:
        model = league_models.Signing
        fields = ('player', 'team', 'begin', 'end', 'attributes')


class JourneeHdrSerializer(serializers.ModelSerializer):
    class Meta:
        model = l1models.Journee
        fields = ('id', 'numero', 'debut', 'fin')


class DayHdrSerializer(serializers.ModelSerializer):
    journee = JourneeHdrSerializer()

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('id', 'number', 'journee')


class TeamDayScoreSerializer(serializers.ModelSerializer):
    team = TeamHdrSerializer()
    day = DayHdrSerializer()
    compo = serializers.SerializerMethodField()
    formation = serializers.SerializerMethodField()

    def get_formation(self, obj):
        return json.loads(obj.attributes)['formation']

    def get_compo(self, obj):
        return json.loads(obj.attributes)['composition']

    class Meta:
        model = league_models.TeamDayScore
        fields = ('team', 'score', 'day', 'formation', 'compo')


class TeamDetailSerializer(serializers.ModelSerializer):
    signings = SigningSerializer(source='signing_set', many=True, read_only=True)
    scores = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)

    class Meta:
        model = league_models.Team
        fields = ('name', 'signings', 'scores')