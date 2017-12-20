from rest_framework import serializers
from dry_rest_permissions.generics import DRYPermissionsField
from django.db import models
from game.services import scoring
from django.contrib.auth.models import User
from . import expandable

# import json

from game.models import league_models, transfer_models, scoring_models
from ligue1 import models as l1models
from utils.timer import Timer


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = l1models.Club
        fields = ('id', 'nom',
                  'maillot_svg', 'maillot_color_bg', 'maillot_color1'
                  )


class ClubHdrSerializer(serializers.ModelSerializer):
    class Meta:
        model = l1models.Club
        fields = ('id', 'nom')


class PlayerHdrSerializer(serializers.HyperlinkedModelSerializer):
    club = ClubHdrSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='stat_joueur-detail')

    class Meta:
        model = l1models.Joueur
        fields = ('id', 'url', 'prenom', 'nom', 'surnom', 'display_name', 'poste', 'club')


class JourneeScoringSerializer(serializers.ModelSerializer):
    journee = serializers.SlugRelatedField('numero', read_only=True)

    class Meta:
        model = scoring_models.JourneeScoring
        fields = ('journee',)


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
        fields = ('id',
                  'url',
                  'prenom',
                  'nom',
                  'surnom',
                  'display_name',
                  'poste',
                  'club',
                  'perfs_agg'
                  # 'perfs',
                  )


class TeamManagerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = league_models.LeagueMembership
        fields = ('user',)


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
    rank = serializers.SerializerMethodField()
    previous_rank = serializers.SerializerMethodField()
    missing_notes = serializers.SerializerMethodField()
    previous_score = serializers.SerializerMethodField()

    def get_is_complete(self, obj):
        return self._compute_is_complete(obj.attributes)

    def get_missing_notes(self, obj):
        """
        Count missing notes in team
        """
        with Timer(id='get_missing_notes', verbose=False):
            if not self.get_is_complete(obj):
                return None
            attrs = obj.attributes
            phase_type = obj.day.league_instance_phase.type
            jfirst = obj.day.league_instance_phase.journee_first
            jlast = obj.day.league_instance_phase.journee_last
            target_nb_per_player = obj.day.league_instance_phase.league_instance.configuration['notes'][phase_type]
            # missing = 0
            joueur_ids = []
            for pos, req_nb in attrs['formation'].items():
                for i in range(min(req_nb, len(attrs['composition'][pos]))):
                    joueur_ids.append(attrs['composition'][pos][i]['player']['id'])
                    # missing += max([(target_nb_per_player - scoring_models.JJScore.objects.count_notes(
                    #     obj.day.league_instance_phase.league_instance.saison, player, journee_first=jfirst,
                    #     journee_last=jlast)), 0])
            return max([((target_nb_per_player * len(joueur_ids)) - scoring_models.JJScore.objects.count_notes(
                obj.day.league_instance_phase.league_instance.saison, joueur_ids, target_nb_per_player,
                journee_first=jfirst,
                journee_last=jlast)), 0])

    @staticmethod
    def _compute_is_complete(tds_attrs):
        # for each position in 'formation', check if there is enough players in 'composition'
        for pos, req_nb in tds_attrs['formation'].items():
            if len(tds_attrs['composition'][pos]) < req_nb:
                return False
        return True

    def _compute_rank(self, tds):
        """
        Compute the rank of this Team[DayScore] within its division
        """
        with Timer(id='_compute_rank', verbose=False):
            if not self.get_is_complete(tds):
                return None
            ordered_ids = list(
                league_models.TeamDayScore.objects.filter(day=tds.day, team__division=tds.team.division).order_by(
                    '-score').values_list('id', flat=True))
            return ordered_ids.index(tds.id) + 1

    def get_rank(self, obj):
        return self._compute_rank(obj)

    def get_previous_rank(self, obj):
        return self._compute_rank(
            league_models.TeamDayScore.objects.filter(day__journee__numero__lt=obj.day.journee.numero,
                                                      day__league_instance_phase=obj.day.league_instance_phase,
                                                      team=obj.team).first())

    def get_previous_score(self, obj):
        pd = league_models.TeamDayScore.objects.filter(day__journee__numero__lt=obj.day.journee.numero,
                                                       day__league_instance_phase=obj.day.league_instance_phase,
                                                       team=obj.team).first()
        if pd:
            return pd.score
        else:
            return None

    class Meta:
        model = league_models.TeamDayScore
        fields = ('team', 'score', 'previous_score', 'is_complete', 'rank', 'previous_rank', 'missing_notes',)
        list_serializer_class = TeamDayScoreByDivisionSerializer


class LeagueInstancePhaseDaySerializer(serializers.ModelSerializer):
    phase_name = serializers.SlugRelatedField(source='league_instance_phase', slug_field='name', read_only=True)
    results = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('league_instance_phase', 'phase_name', 'number', 'results')


class PhaseDayRankingSerializer(serializers.ModelSerializer):
    teamdayscore_set = TeamDayScoreSerializer(many=True, read_only=True)

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('number', 'league_instance_phase', 'teamdayscore_set')


class PhaseRankingSerializer(serializers.ModelSerializer):
    # leagueinstancephaseday_set = PhaseDayRankingSerializer(many=True, read_only=True)
    current_ranking = serializers.SerializerMethodField()
    #previous_ranking = serializers.SerializerMethodField()

    @staticmethod
    def _get_latest_day(obj):
        return league_models.LeagueInstancePhaseDay.objects.select_related('journee').filter(
            league_instance_phase=obj).order_by('-journee__numero').first()

    def get_current_ranking(self, obj):
        # latest_day = league_models.LeagueInstancePhaseDay.objects.filter(league_instance_phase=obj).order_by(
        #     '-journee__numero').first()
        return PhaseDayRankingSerializer(context={'request': self.context['request']}).to_representation(
            self._get_latest_day(obj))

    # def get_previous_ranking(self, obj):
    #     latest = self._get_latest_day(obj)
    #     if latest:
    #         previous_day = league_models.LeagueInstancePhaseDay.objects.filter(league_instance_phase=obj,
    #                                                                            journee__numero__lt=latest.journee.numero).order_by(
    #             '-journee__numero').first()
    #     return PhaseDayRankingSerializer(context={'request': self.context['request']}).to_representation(previous_day)

    class Meta:
        model = league_models.LeagueInstancePhase
        fields = ('id', 'name', 'type', 'journee_first', 'journee_last', 'league_instance',  # __all__
                  'current_ranking',)


class LeagueInstanceRankingSerializer(serializers.ModelSerializer):
    leagueinstancephase_set = PhaseRankingSerializer(many=True, read_only=True)

    class Meta:
        model = league_models.LeagueInstance
        fields = ('id', 'name', 'slogan', 'league', 'current', 'begin', 'end', 'saison', 'configuration',  # __all__
                  'leagueinstancephase_set',)


class SigningSerializer(serializers.ModelSerializer):
    player = PlayerHdrSerializer()
    team = TeamHdrSerializer()

    class Meta:
        model = league_models.Signing
        fields = ('id', 'player', 'team', 'begin', 'end', 'attributes')


class JourneeHdrSerializer(serializers.ModelSerializer):
    is_last = serializers.SerializerMethodField()
    is_first = serializers.SerializerMethodField()

    def get_is_last(self, obj):
        return l1models.Journee.objects.filter(saison=obj.saison, numero__gt=obj.numero).count() == 0

    def get_is_first(self, obj):
        return l1models.Journee.objects.filter(saison=obj.saison, numero__lt=obj.numero).count() == 0

    class Meta:
        model = l1models.Journee
        fields = ('id', 'numero', 'debut', 'fin', 'is_last', 'is_first')


class DayHdrSerializer(serializers.ModelSerializer):
    journee = JourneeHdrSerializer()
    phase = serializers.SlugRelatedField(source='league_instance_phase', slug_field='name', read_only=True)
    phase_id = serializers.PrimaryKeyRelatedField(source='league_instance_phase', read_only=True)

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('id', 'number', 'journee', 'phase_id', 'phase',)


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
        return transfer_models.Release.objects.get_for_team(value, just_count=True)


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
    latest_scores = serializers.SerializerMethodField()
    managers = TeamManagerSerializer(many=True, read_only=True)
    account_balance = serializers.SlugRelatedField(source='bank_account', slug_field='balance', read_only=True)

    def get_latest_scores(self, obj):
        try:
            linstance = league_models.LeagueInstance.objects.get(league=obj.league, current=True)
            days = league_models.LeagueInstancePhaseDay.objects.filter(
                league_instance_phase__league_instance=linstance).filter(
                journee__numero=league_models.LeagueInstancePhaseDay.objects.filter(
                    league_instance_phase__league_instance=linstance).order_by('-journee__numero').values_list(
                    'journee__numero', flat=True).first())
            return TeamDayScoreSerializer(many=True, read_only=True,
                                          context={'request': self.context['request']}).to_representation(
                league_models.TeamDayScore.objects.filter(day__in=days, team=obj).order_by(
                    'day__league_instance_phase'))
        except league_models.LeagueInstance.DoesNotExist:
            return None

    class Meta:
        model = league_models.Team
        fields = ('id', 'name', 'attributes', 'managers', 'permissions', 'account_balance', 'signings_aggregation',
                  'signings', 'latest_scores',)


class BankAccountHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = league_models.BankAccountHistory
        fields = ('date', 'amount', 'new_balance', 'info')


class ReleaseSerializer(serializers.ModelSerializer):
    signing = SigningSerializer(read_only=True)

    class Meta:
        model = transfer_models.Release
        fields = ('signing', 'amount',)


class MerkatoSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = transfer_models.MerkatoSession
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    player = PlayerHdrSerializer(read_only=True)
    team = TeamHdrSerializer(read_only=True)
    merkato_session = MerkatoSessionSerializer(read_only=True)

    class Meta:
        model = transfer_models.Sale
        fields = '__all__'
