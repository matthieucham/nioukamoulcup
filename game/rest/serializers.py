import operator
from rest_framework import serializers
from rest_framework.reverse import reverse
from dry_rest_permissions.generics import DRYPermissionsField
from django.db import models
from django.utils.timezone import localtime, now

from game.models import league_models, transfer_models, scoring_models
from ligue1 import models as l1models
from game.services import auctions
from utils.timer import timed
import simplejson as json


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = l1models.Club
        fields = ('id', 'nom',
                  'maillot_svg', 'maillot_color_bg', 'maillot_color_stroke'
                  )


class PlayerHdrSerializer(serializers.HyperlinkedModelSerializer):
    club = ClubSerializer()
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
        try:
            perfs = scoring_models.SJScore.objects.filter(joueur=value,
                                                          saison_scoring__saison__est_courante__isnull=False).get()
        except scoring_models.SJScore.DoesNotExist:
            return {'NOTES_COUNT': 0, 'NOTES_AVG': None}
        output = {'NOTES_COUNT': perfs.nb_notes, 'NOTES_AVG': perfs.avg_note}
        for bonuskey, bonusval in perfs.details.items():
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


class TeamHyperLink(serializers.HyperlinkedRelatedField):
    view_name = 'league_team-detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'pk': obj.league.pk,
            'team_pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class TeamHdrSerializer(serializers.ModelSerializer):
    url = TeamHyperLink(source='*', read_only=True)

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
        # divs = list()
        for div in league_models.LeagueDivision.objects.filter(
                league=one_tds.day.league_instance_phase.league_instance.league).order_by('level'):
            div_ranking = super().to_representation(
                league_models.TeamDayScore.objects.filter(day=one_tds.day, team__division=div,
                                                          current=one_tds.current).order_by('-score'))
            # divs.append({'id': div.id, 'name': div.name, 'level': div.level, 'ranking': div_ranking})
            yield {'id': div.id, 'name': div.name, 'level': div.level, 'ranking': div_ranking}
        # return divs


class TeamDayScoreSerializer(serializers.ModelSerializer):
    team = TeamHdrSerializer(read_only=True)
    is_complete = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    previous_rank = serializers.SerializerMethodField()
    missing_notes = serializers.SerializerMethodField()
    previous_score = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(TeamDayScoreSerializer, self).__init__(*args, **kwargs)
        expand_attributes = self.context.get('expand_attributes', False)
        if not expand_attributes:
            self.fields.pop('attributes')

    def get_is_complete(self, obj):
        if not obj:
            return False
        return self._compute_is_complete(obj.attributes)

    def get_missing_notes(self, obj):
        """
        Count missing notes in team
        """
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

    def _compute_rank(self, tds, current):
        """
        Compute the rank of this Team[DayScore] within its division
        """
        if not self.get_is_complete(tds):
            return None
        if league_models.TeamDayScore.objects.filter(day=tds.day, team__division=tds.team.division,
                                                     current=current).count() > 0:
            unfiltered = league_models.TeamDayScore.objects.filter(day=tds.day, team__division=tds.team.division,
                                                                   current=current).order_by('-score').all()
        else:
            unfiltered = league_models.TeamDayScore.objects.filter(day=tds.day,
                                                                   team__division=tds.team.division).order_by(
                '-score').all()
        ordered_ids = [item.id for item in unfiltered if self.get_is_complete(item)]
        # ordered_ids = list(
        #     league_models.TeamDayScore.objects.filter(day=tds.day, team__division=tds.team.division, current=current).order_by(
        #         '-score').values_list('id', flat=True))
        return ordered_ids.index(tds.id) + 1

    def get_rank(self, obj):
        return self._compute_rank(obj, True)

    def get_previous_rank(self, obj):
        return self._compute_rank(
            league_models.TeamDayScore.objects.filter(day__journee__numero__lt=obj.day.journee.numero,
                                                      day__league_instance_phase=obj.day.league_instance_phase,
                                                      current=False,
                                                      team=obj.team).first(), False)

    def get_previous_score(self, obj):
        pd = league_models.TeamDayScore.objects.filter(day__journee__numero__lt=obj.day.journee.numero,
                                                       day__league_instance_phase=obj.day.league_instance_phase,
                                                       current=False,
                                                       team=obj.team).first()
        if pd:
            return pd.score
        else:
            return None

    class Meta:
        model = league_models.TeamDayScore
        fields = (
            'team', 'score', 'previous_score', 'is_complete', 'rank', 'previous_rank', 'missing_notes', 'current',
            'attributes')
        list_serializer_class = TeamDayScoreByDivisionSerializer


class LeagueInstancePhaseDaySerializer(serializers.ModelSerializer):
    phase_name = serializers.SlugRelatedField(source='league_instance_phase', slug_field='name', read_only=True)
    # results = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)
    results = serializers.SerializerMethodField()

    def get_results(self, obj):
        # show_current = obj.league_instance_phase.league_instance.league.mode == 'KCUP'
        show_current = True  # TODO à optimiser pour le futur mode FSY
        if obj.teamdayscore_set.filter(current=show_current).count() > 0:
            return TeamDayScoreSerializer(context={'request': self.context['request']}, many=True,
                                          read_only=True).to_representation(
                obj.teamdayscore_set.filter(current=show_current))
        else:
            return TeamDayScoreSerializer(context={'request': self.context['request']}, many=True,
                                          read_only=True).to_representation(obj.teamdayscore_set.all())

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('league_instance_phase', 'phase_name', 'number', 'results')


class PlayerWithScoreSerializer(PlayerHdrSerializer):
    scores = serializers.SerializerMethodField()

    def get_scores(self, obj):
        result = dict()
        for scoph in self.context['score_by_id'][obj.id]['scores']:
            result.update({scoph['phase']: scoph['score']})
        return result

    class Meta:
        model = l1models.Joueur
        fields = ('id', 'url', 'prenom', 'nom', 'surnom', 'display_name', 'poste', 'club', 'scores')


class PhaseDayPlayersRankingSerializer(serializers.ModelSerializer):
    ranking = serializers.SerializerMethodField()

    @timed
    def get_ranking(self, obj):
        score_by_id = dict()
        # fetch scores
        for tds in obj.teamdayscore_set.all():
            if tds.attributes and 'composition' in tds.attributes:
                for poste in ['G', 'D', 'M', 'A']:
                    for psco in tds.attributes['composition'][poste]:
                        score_by_id.update({psco['player']['id']: psco['score']})
        sorted_by_scores = sorted(score_by_id.items(), key=operator.itemgetter(1), reverse=True)
        # fetch players
        players = l1models.Joueur.objects.select_related('club').filter(
            pk__in=[key for key, _ in score_by_id.items()])
        return PlayerWithScoreSerializer(
            many=True, read_only=True,
            context={'request': self.context['request'], 'score_by_id': score_by_id,
                     'sorted_by_scores': sorted_by_scores}).to_representation(players)

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('ranking',)


class PhaseDayRankingSerializer(serializers.ModelSerializer):
    # ranking_ekyps = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)
    ranking_ekyps = serializers.SerializerMethodField()

    # ranking_players = PhaseDayPlayersRankingSerializer(source='*')

    def get_ranking_ekyps(self, obj):
        # show_current = obj.league_instance_phase.league_instance.league.mode == 'KCUP'
        show_current = True  # TODO à optimiser pour le futur mode FSY
        if obj.teamdayscore_set.filter(current=show_current).count() > 0:
            return TeamDayScoreSerializer(context={'request': self.context['request'], 'show_current': show_current,
                                                   'expand_attributes': self.context.get('expand_attributes', False)},
                                          many=True,
                                          read_only=True).to_representation(
                obj.teamdayscore_set.filter(current=show_current))
        else:
            return TeamDayScoreSerializer(context={'request': self.context['request'], 'show_current': show_current,
                                                   'expand_attributes': self.context.get('expand_attributes', False)},
                                          many=True,
                                          read_only=True).to_representation(
                obj.teamdayscore_set.all())

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('number', 'league_instance_phase', 'ranking_ekyps')


class PhaseRankingSerializer(serializers.ModelSerializer):
    current_ranking = serializers.SerializerMethodField()

    @staticmethod
    def _get_latest_day(obj):
        return league_models.LeagueInstancePhaseDay.objects.select_related('journee').prefetch_related(
            'teamdayscore_set').filter(league_instance_phase=obj).order_by('-journee__numero').first()

    @timed
    def get_current_ranking(self, obj):
        return PhaseDayRankingSerializer(context={'request': self.context['request'],
                                                  'expand_attributes': self.context.get('expand_attributes',
                                                                                        False)}).to_representation(
            self._get_latest_day(obj))

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
    is_current = serializers.SerializerMethodField()

    def get_is_last(self, obj):
        return l1models.Journee.objects.filter(saison=obj.saison, numero__gt=obj.numero).count() == 0

    def get_is_first(self, obj):
        return l1models.Journee.objects.filter(saison=obj.saison, numero__lt=obj.numero).count() == 0

    def get_is_current(self, obj):
        return self.context.get('current', False)

    class Meta:
        model = l1models.Journee
        fields = ('id', 'numero', 'debut', 'fin', 'is_last', 'is_first', 'is_current')


class DayHdrSerializer(serializers.ModelSerializer):
    # journee = JourneeHdrSerializer()
    journee = serializers.SerializerMethodField()
    phase = serializers.SlugRelatedField(source='league_instance_phase', slug_field='name', read_only=True)
    phase_id = serializers.PrimaryKeyRelatedField(source='league_instance_phase', read_only=True)

    def get_journee(self, obj):
        return JourneeHdrSerializer(
            context={'request': self.context.get('request'), 'current': self.context.get('current')}).to_representation(
            obj.journee
        )

    class Meta:
        model = league_models.LeagueInstancePhaseDay
        fields = ('id', 'number', 'journee', 'phase_id', 'phase',)


class TeamDayCompoAndScoreSerializer(serializers.ModelSerializer):
    team = TeamHdrSerializer()
    day = serializers.SerializerMethodField()
    compo = serializers.SerializerMethodField()
    formation = serializers.SerializerMethodField()

    def get_day(self, obj):
        return DayHdrSerializer(
            context={'request': self.context['request'], 'current': self.context['current']}).to_representation(
            obj.day)

    def get_formation(self, obj):
        return obj.attributes['formation']

    def get_compo(self, obj):
        return obj.attributes['composition']

    class Meta:
        model = league_models.TeamDayScore
        fields = ('team', 'score', 'day', 'formation', 'compo')


class TotalPASaleField(serializers.Field):
    def to_representation(self, value):
        return transfer_models.Sale.objects.get_for_team(value, just_count=True)


class TotalReleaseField(serializers.Field):
    def to_representation(self, value):
        return transfer_models.Release.objects.get_for_team(value, just_count=True)


class TotalSignings(serializers.Field):
    def to_representation(self, value):
        return league_models.Signing.objects.filter(team=value,
                                                    league_instance=league_models.LeagueInstance.objects.get_current(
                                                        value.league)).count()


class CurrentSignings(serializers.Field):
    def to_representation(self, value):
        total = 0
        output = dict()
        for spcount in league_models.Signing.objects.filter(team=value, end__isnull=True,
                                                            league_instance=league_models.LeagueInstance.objects.get_current(
                                                                value.league)).values(
            'player__poste').annotate(models.Count('player')):
            total += spcount['player__count']
            output.update({spcount['player__poste']: spcount['player__count']})
        output.update({'total': total})
        return output


class SigningsAggregationSerializer(serializers.Serializer):
    total_pa = TotalPASaleField(source='*')
    total_releases = TotalReleaseField(source='*')
    total_signings = TotalSignings(source='*')
    current_signings = CurrentSignings(source='*')


class TeamDetailSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField(additional_actions=['release'], )
    signings_aggregation = SigningsAggregationSerializer(source='*', read_only=True)
    signings = SigningSerializer(source='signing_set', many=True, read_only=True)
    latest_scores = serializers.SerializerMethodField()
    managers = TeamManagerSerializer(many=True, read_only=True)
    account_balance = serializers.SlugRelatedField(source='bank_account', slug_field='balance', read_only=True)

    def get_latest_scores(self, obj):
        try:
            linstance = league_models.LeagueInstance.objects.get(league=obj.league, current=True)
            latest_day_by_phase = league_models.LeagueInstancePhase.objects.filter(league_instance=linstance).annotate(
                latest_day=models.Max('leagueinstancephaseday__journee__numero'))
            days = []
            for ph in latest_day_by_phase.all():
                days += league_models.LeagueInstancePhaseDay.objects.filter(
                    league_instance_phase__league_instance=linstance).filter(league_instance_phase=ph.pk,
                                                                             journee__numero=ph.latest_day)
            return TeamDayCompoAndScoreSerializer(many=True, read_only=True,
                                                  context={'request': self.context['request'],
                                                           'current': self.context['current']}).to_representation(
                league_models.TeamDayScore.objects.filter(day__in=days, team=obj,
                                                          current=self.context['current']).select_related('team',
                                                                                                          'day').order_by(
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


class TeamInfoByDivisionSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        """
        List of instances (team) -> grouped by team.division
        """
        iterable = instance.all() if isinstance(instance, models.Manager) else instance
        if not iterable:
            return super().to_representation(instance)
        one_team = iterable[0]
        for div in league_models.LeagueDivision.objects.filter(
                league=one_team.league).order_by('level'):
            div_teams = super().to_representation(
                league_models.Team.objects.filter(division=div).order_by('name'))
            yield {'id': div.id, 'name': div.name, 'teams': div_teams}


class TeamInfoSerializer(TeamHdrSerializer):
    balance = serializers.SlugRelatedField('balance', source='bank_account', read_only=True)
    # total_pa = TotalPASaleField(source='*')
    # total_releases = TotalReleaseField(source='*')
    current_signings = CurrentSignings(source='*')
    division = serializers.SlugRelatedField('name', read_only=True)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('bank_account').select_related('division')
        return queryset

    class Meta:
        model = league_models.Team
        fields = ('id', 'url', 'name', 'attributes', 'division', 'balance', 'current_signings',)
        list_serializer_class = TeamInfoByDivisionSerializer


class LeagueInstancePhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = league_models.LeagueInstancePhase
        fields = ('id', 'name', 'league_instance')


class NewPlayersRankingSerializer(PlayerHdrSerializer):
    scores = serializers.SerializerMethodField()

    def get_scores(self, obj):
        result = dict()
        for ph in self.context['phases']:
            try:
                phase_found = False
                for scoph in self.context['scoring_map'][obj.id]['scores']:
                    if scoph['phase'] == ph['id']:
                        result.update({scoph['phase']: scoph['score']})
                        phase_found = True
                if not phase_found:
                    result.update({ph['id']: None})
            except KeyError:
                result.update({ph['id']: None})
        return result

    class Meta:
        model = l1models.Joueur
        fields = (
            'id',
            'url',
            'prenom',
            'nom',
            'surnom',
            'display_name',
            'poste',
            'club',
            'scores',
        )


class AuctionSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField()

    def get_is_mine(self, obj):
        if 'request' in self.context:
            mb = league_models.LeagueMembership.objects.filter(team=obj.team, user=self.context['request'].user).first()
            return mb is not None
        return None

    class Meta:
        model = transfer_models.Auction
        fields = ('value', 'is_valid', 'is_mine')


class SaleSummarySerializer(serializers.ModelSerializer):
    author = TeamHdrSerializer(source='team', read_only=True)
    player = PlayerHdrSerializer(read_only=True)

    class Meta:
        model = transfer_models.Sale
        fields = ('id', 'rank', 'type', 'player', 'author', 'min_price')


class SaleSummaryWithMyAuctionSerializer(SaleSummarySerializer):
    my_auction = serializers.SerializerMethodField()
    created_by_me = serializers.SerializerMethodField()

    def get_my_auction(self, obj):
        if 'request' in self.context:
            mb = league_models.LeagueMembership.objects.get(user=self.context['request'].user)
            try:
                return transfer_models.Auction.objects.get(sale=obj, team=mb.team).value
            except transfer_models.Auction.DoesNotExist:
                return None
        return None

    def get_created_by_me(self, obj):
        if 'team' in self.context:
            return obj.team.pk == self.context.get('team').pk
        return None

    class Meta(SaleSummarySerializer.Meta):
        fields = SaleSummarySerializer.Meta.fields + ('my_auction', 'created_by_me',)


class SaleSerializer(SaleSummarySerializer):
    winner = serializers.SerializerMethodField()
    amount = serializers.SlugRelatedField(source='winning_auction', slug_field='value', read_only=True)
    auctions = serializers.SerializerMethodField()
    date = serializers.SlugRelatedField(source='merkato_session', slug_field='closing', read_only=True)

    def get_auctions(self, obj):
        return AuctionSerializer(transfer_models.Auction.objects.filter(sale=obj).order_by('value'), read_only=True,
                                 many=True, context=self.context).data

    def get_winner(self, obj):
        if obj.winning_auction:
            return TeamHdrSerializer(obj.winning_auction.team, read_only=True, context=self.context).data
        return None

    class Meta:
        model = transfer_models.Sale
        fields = (
            'id', 'rank', 'type', 'player', 'author', 'min_price', 'date', 'winner', 'amount', 'auctions')


class MerkatoSessionSummarySerializer(serializers.HyperlinkedModelSerializer):
    sales_count = serializers.SerializerMethodField()
    releases_count = serializers.SerializerMethodField()

    def get_sales_count(self, obj):
        return transfer_models.Sale.objects.filter(merkato_session=obj).count()

    def get_releases_count(self, obj):
        return transfer_models.Release.objects.filter(merkato_session=obj, done=True).count()

    class Meta:
        model = transfer_models.MerkatoSession
        fields = ('url', 'number', 'closing', 'solving', 'is_solved', 'attributes', 'sales_count', 'releases_count')


class MerkatoSessionSerializer(MerkatoSessionSummarySerializer):
    sales = serializers.SerializerMethodField()
    releases = serializers.SerializerMethodField()

    def get_sales(self, obj):
        ordered_sales = transfer_models.Sale.objects.filter(merkato_session=obj).order_by('rank')
        return SaleSerializer(ordered_sales, many=True, read_only=True, context=self.context).data

    def get_releases(self, obj):
        ordered_rel = transfer_models.Release.objects.filter(merkato_session=obj, done=True)
        return ReleaseSerializer(ordered_rel, many=True, read_only=True, context=self.context).data

    class Meta:
        model = transfer_models.MerkatoSession
        fields = (
            'url', 'number', 'closing', 'solving', 'is_solved', 'attributes', 'sales_count', 'releases_count', 'sales',
            'releases',)


class MerkatoSerializer(serializers.ModelSerializer):
    sessions = serializers.SerializerMethodField()

    def get_sessions(self, obj):
        ordered_sessions = transfer_models.MerkatoSession.objects.filter(merkato=obj, is_solved=True).order_by('number')
        return MerkatoSessionSummarySerializer(ordered_sessions, many=True, read_only=True, context=self.context).data

    class Meta:
        model = transfer_models.Merkato
        fields = ('begin', 'end', 'mode', 'configuration', 'league_instance', 'sessions',)


class BasePlayerForPickerSerializer(PlayerHdrSerializer):
    current_signing = serializers.SerializerMethodField()
    current_sale = serializers.SerializerMethodField()

    def get_current_signing(self, obj):
        raise NotImplementedError('Override me')

    def get_current_sale(self, obj):
        raise NotImplementedError('Override me')

    class Meta:
        model = l1models.Joueur
        fields = (
            'id',
            'url',
            'prenom',
            'nom',
            'surnom',
            'display_name',
            'poste',
            'club',
            'current_signing',
            'current_sale',
        )


class PlayerMerkatoSerializer(BasePlayerForPickerSerializer):

    def get_current_signing(self, obj):
        signing = self.context.get('signings_map').get(obj.id) or None
        if signing is not None:
            return {'team': signing}
        else:
            return None

    def get_current_sale(self, obj):
        sale = self.context.get('sales_map').get(obj.id) or None
        if sale is not None:
            return {'team': sale}
        else:
            return None

    class Meta(BasePlayerForPickerSerializer.Meta):
        pass


class PlayerForMVSerializer(BasePlayerForPickerSerializer):

    def get_current_signing(self, obj):
        return None

    def get_current_sale(self, obj):
        sale = self.context.get('sales_map').get(obj.id) or None
        if sale is not None:
            return {'team': sale}
        else:
            return None

    class Meta(BasePlayerForPickerSerializer.Meta):
        pass


class OpenMerkatoSessionSerializer(MerkatoSessionSummarySerializer):
    sales = serializers.SerializerMethodField()

    def get_sales(self, obj):
        ordered_sales = transfer_models.Sale.objects.filter(merkato_session=obj).order_by('rank')
        return SaleSummaryWithMyAuctionSerializer(ordered_sales, many=True, read_only=True, context=self.context).data

    class Meta(MerkatoSessionSummarySerializer.Meta):
        model = transfer_models.MerkatoSession
        fields = MerkatoSessionSummarySerializer.Meta.fields + ('sales',)


class DraftPickSerializer(serializers.ModelSerializer):
    player = PlayerHdrSerializer(read_only=True)

    class Meta:
        model = transfer_models.DraftPick
        fields = ('pick_order', 'player',)


class OpenDraftSessionRankSerializer(serializers.ModelSerializer):
    picks = DraftPickSerializer(many=True, read_only=True)

    class Meta:
        model = transfer_models.DraftSessionRank
        fields = ('rank', 'picks',)


class OpenDraftSessionSerializer(serializers.HyperlinkedModelSerializer):
    my_rank = serializers.SerializerMethodField()

    def get_my_rank(self, obj):
        if 'team' in self.context:
            try:
                return OpenDraftSessionRankSerializer(
                    transfer_models.DraftSessionRank.objects.get(draft_session=obj, team=self.context['team']),
                    many=False,
                    read_only=True, context={'request': self.context['request']}).data
            except transfer_models.DraftSessionRank.DoesNotExist:
                return None
        return None

    class Meta:
        model = transfer_models.DraftSession
        fields = ('id', 'number', 'closing', 'my_rank',)


class DraftSessionRankSerializer(serializers.ModelSerializer):
    team = TeamHdrSerializer(read_only=True)
    signing = SigningSerializer(read_only=True)

    class Meta:
        model = transfer_models.DraftSessionRank
        fields = ('rank', 'team', 'signing')


class DraftSessionSerializer(serializers.ModelSerializer):
    draftsessionrank_set = DraftSessionRankSerializer(read_only=True, many=True)

    class Meta:
        model = transfer_models.DraftSession
        fields = (
            'number', 'closing', 'is_solved', 'attributes', 'draftsessionrank_set',)


class TransitionTeamChoiceSerializer(serializers.ModelSerializer):
    signings_to_free = SigningSerializer(many=True, read_only=True)

    class Meta:
        model = transfer_models.TransitionTeamChoice
        fields = ('formation_to_choose', 'signings_to_free',)


class TransitionSessionSerializer(serializers.ModelSerializer):
    my_choice = serializers.SerializerMethodField()

    def get_my_choice(self, obj):
        if 'team' in self.context:
            try:
                return TransitionTeamChoiceSerializer(
                    transfer_models.TransitionTeamChoice.objects.get(transition_session=obj, team=self.context['team']),
                    many=False,
                    read_only=True, context={'request': self.context['request']}
                ).data
            except transfer_models.TransitionTeamChoice.DoesNotExist:
                return None
        return None

    class Meta:
        model = transfer_models.TransitionSession
        fields = ('closing', 'is_solved', 'attributes', 'my_choice',)


class CurrentMerkatoSerializer(serializers.ModelSerializer):
    sessions = serializers.SerializerMethodField()
    draft_sessions = serializers.SerializerMethodField()
    transition_sessions = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    account_balance = serializers.SerializerMethodField()

    def get_account_balance(self, obj):
        try:
            account = self.context.get('team').bank_account
            return {
                'balance': account.balance,
                'locked': account.blocked
            }
        except league_models.BankAccount.DoesNotExist:
            return None

    def get_sessions(self, obj):
        ordered_sessions = transfer_models.MerkatoSession.objects.filter(merkato=obj, is_solved=False,
                                                                         solving__gt=localtime(now())).annotate(
            num_sales=models.Count('sale')).filter(num_sales__gt=0).order_by('number')
        return OpenMerkatoSessionSerializer(ordered_sessions, many=True, read_only=True, context=self.context).data

    def get_draft_sessions(self, obj):
        ordered_sessions = transfer_models.DraftSession.objects.filter(merkato=obj, is_solved=False,
                                                                       closing__gt=localtime(now())).order_by('number')
        return OpenDraftSessionSerializer(ordered_sessions, many=True, read_only=True, context=self.context).data

    def get_transition_sessions(self, obj):
        ordered_sessions = transfer_models.TransitionSession.objects.filter(merkato=obj, is_solved=False,
                                                                            closing__gt=localtime(now()))
        return TransitionSessionSerializer(ordered_sessions, many=True, read_only=True, context=self.context).data

    def get_permissions(self, obj):
        auc, auc_reason = auctions.can_register_auction(self.context.get('team'), obj)
        pa, pa_reason = auctions.can_register_pa(self.context.get('team'), obj)
        mv, mv_reason = auctions.can_register_mv(self.context.get('team'), obj)
        return {
            'auctions': {
                'can': auc,
                'reason': auc_reason
            },
            'pa': {
                'can': pa,
                'reason': pa_reason
            },
            'mv': {
                'can': mv,
                'reason': mv_reason
            },
            'next_session': MerkatoSessionSummarySerializer(
                transfer_models.MerkatoSession.objects.get_next_available(obj), read_only=True,
                context=self.context).data
        }

    class Meta:
        model = transfer_models.Merkato
        fields = (
            'id',
            'begin',
            'end',
            'last_solving',
            'mode',
            'configuration',
            'league_instance',
            'account_balance',
            'sessions',
            'draft_sessions',
            'transition_sessions',
            'permissions',)


class PalmaresSerializer(serializers.ModelSerializer):
    final_ranking = serializers.SerializerMethodField()
    players_ranking = serializers.SerializerMethodField()
    signings_history = serializers.SerializerMethodField()

    def get_final_ranking(self, obj):
        return json.loads(obj.final_ranking)

    def get_players_ranking(self, obj):
        return json.loads(obj.players_ranking)

    def get_signings_history(self, obj):
        return json.loads(obj.signings_history)

    class Meta:
        model = league_models.Palmares
        fields = '__all__'
