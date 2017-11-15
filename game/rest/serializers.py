from rest_framework import serializers
from dry_rest_permissions.generics import DRYPermissionsField
from django.db import models
from game.services import scoring
from django.contrib.auth.models import User


# import json

from game.models import league_models, transfer_models, scoring_models
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


class JourneeScoringSerializer(serializers.ModelSerializer):
    journee = serializers.SlugRelatedField('numero', read_only=True)

    class Meta:
        model = scoring_models.JourneeScoring
        fields = ('journee', )


class JJScoreSerializer(serializers.ModelSerializer):
    journee_scoring = JourneeScoringSerializer(read_only=True)
    note = serializers.FloatField()
    bonus = serializers.FloatField()
    compensation = serializers.FloatField()

    class Meta:
        model = scoring_models.JJScore
        fields = ('journee_scoring', 'note', 'bonus', 'compensation', 'details')


class PlayerScoreSerializer(PlayerHdrSerializer):
    # perfs = JJScoreSerializer(source='jjscore_set', many=True, read_only=True)
    perfs_agg = serializers.SerializerMethodField(source='*')

    def get_perfs_agg(self, value):
        perfs = scoring_models.JJScore.objects.filter(joueur=value,
                                                      journee_scoring__saison_scoring__saison__est_courante__isnull=False)
        perfs_notes = list(filter(lambda n: n is not None, map(lambda jjs: jjs.note, perfs)))
        count = len(perfs_notes)
        avg = round(float(sum(perfs_notes)) / max(count, 1), 3)

        output = {'NOTES_COUNT': count, 'NOTES_AVG': avg}
        for metakey in scoring.BONUS:
            for bonuskey in scoring.BONUS[metakey]:
                bonusval = sum(map(lambda bo: bo[bonuskey], filter(lambda bo: bonuskey in bo,
                                                                   map(lambda jjs: jjs.details['bonuses'], filter(
                                                                       lambda j: j.details and 'bonuses' in j.details,
                                                                       perfs)))))
                output.update({bonuskey: bonusval})

        return output

    class Meta:
        model = l1models.Joueur
        fields = ('id', 'url', 'prenom', 'nom', 'surnom', 'poste', 'club', 'perfs_agg')


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
    player = PlayerScoreSerializer()
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
    total_releases = TotalReleaseField(source='*')
    total_signings = TotalSignings(source='*')
    current_signings = CurrentSignings(source='*')


class TeamDetailSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    signings_aggregation = SigningsAggregationSerializer(source='*', read_only=True)
    signings = SigningSerializer(source='signing_set', many=True, read_only=True)
    # scores = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)
    latest_scores = serializers.SerializerMethodField()
    managers = TeamManagerSerializer(many=True, read_only=True)
    account_balance = serializers.SlugRelatedField(source='bank_account', slug_field='balance', read_only=True)

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
        fields = ('name', 'attributes', 'managers', 'permissions', 'account_balance', 'signings_aggregation',
                  'signings', 'latest_scores', )