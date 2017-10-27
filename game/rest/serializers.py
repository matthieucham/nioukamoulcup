from rest_framework import serializers
from dry_rest_permissions.generics import DRYPermissionsField
from django.db import models
from django.contrib.auth.models import User
# import json

from game.models import league_models, transfer_models
from ligue1 import models as l1models


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = l1models.Club
        fields = ('id', 'nom', 'maillot_svg', 'maillot_color_bg', 'maillot_color1', 'maillot_color2')


class ClubHdrSerializer(serializers.ModelSerializer):
    class Meta:
        model = l1models.Club
        fields = ('id', 'nom')


class PlayerHdrSerializer(serializers.HyperlinkedModelSerializer):
    club = ClubHdrSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='stat_joueur-detail')

    class Meta:
        model = l1models.Joueur
        fields = ('id', 'url', 'prenom', 'nom', 'surnom', 'poste', 'club')


class TeamManagerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = league_models.LeagueMembership
        fields = ('user', )


class TeamHdrSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='league_ekyp-detail')

    class Meta:
        model = league_models.Team
        fields = ('id', 'url', 'name',)


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
        attrs = obj.attributes
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
    phase = serializers.SlugRelatedField(source='league_instance_phase', slug_field='name', read_only=True)
    phase_id = serializers.PrimaryKeyRelatedField(source='league_instance_phase', read_only=True)

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('id', 'number', 'journee', 'phase_id', 'phase', )


class TeamDayScoreSerializer(serializers.ModelSerializer):
    team = TeamHdrSerializer()
    day = DayHdrSerializer()
    compo = serializers.SerializerMethodField()
    formation = serializers.SerializerMethodField()

    def get_formation(self, obj):
        return obj.attributes['formation']

    def get_compo(self, obj):
        return obj.attributes['composition']

    class Meta:
        model = league_models.TeamDayScore
        fields = ('team', 'score', 'day', 'formation', 'compo')


class TotalPASaleField(serializers.Field):
    def to_representation(self, value):
        return transfer_models.Sale.objects.filter(team=value, type='PA',
                                                   merkato_session__merkato__league_instance__current=True).count()


class TotalReleaseField(serializers.Field):
    def to_representation(self, value):
        return transfer_models.Release.objects.filter(signing__team=value,
                                                      merkato_session__merkato__league_instance__current=True,
                                                      merkato_session__is_solved=True).count()


class TotalSignings(serializers.Field):
    def to_representation(self, value):
        return league_models.Signing.objects.filter(team=value).count()


class CurrentSignings(serializers.Field):
    def to_representation(self, value):
        return league_models.Signing.objects.filter(team=value, end__isnull=True).count()


class SigningsAggregationSerializer(serializers.Serializer):
    total_pa = TotalPASaleField(source='*')
    total_release = TotalReleaseField(source='*')
    total_signings = TotalSignings(source='*')
    current_signings = CurrentSignings(source='*')


class TeamDetailSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    signings_aggregation = SigningsAggregationSerializer(source='*', read_only=True)
    signings = SigningSerializer(source='signing_set', many=True, read_only=True)
    # scores = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)
    latest_scores = serializers.SerializerMethodField()
    managers = TeamManagerSerializer(many=True, read_only=True)

    def get_latest_scores(self, obj):
        try:
            current_instance = league_models.LeagueInstance.objects.get(league=obj.league, current=True)
            days = league_models.LeagueInstancePhaseDay.objects.get_latest_day_for_phases(
                league_models.LeagueInstancePhase.objects.filter(league_instance=current_instance))
            return TeamDayScoreSerializer(many=True, read_only=True,
                                          context={'request': self.context['request']}).to_representation(
                league_models.TeamDayScore.objects.filter(day__in=days, team=obj))
        except league_models.LeagueInstance.DoesNotExist:
            return None

    class Meta:
        model = league_models.Team
        fields = ('name', 'managers', 'permissions', 'signings_aggregation',
                  'signings', 'latest_scores', )