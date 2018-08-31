import operator
from rest_framework import serializers
from rest_framework.reverse import reverse
from dry_rest_permissions.generics import DRYPermissionsField
from django.db import models

from game.models import league_models, transfer_models, scoring_models
from ligue1 import models as l1models
from utils.timer import timed


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
        for div in league_models.LeagueDivision.objects.filter(
                league=one_tds.day.league_instance_phase.league_instance.league).order_by('level'):
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
        if not obj:
            return False
        return self._compute_is_complete(obj.attributes)

    @timed
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

    def _compute_rank(self, tds):
        """
        Compute the rank of this Team[DayScore] within its division
        """
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
    ranking_ekyps = TeamDayScoreSerializer(source='teamdayscore_set', many=True, read_only=True)

    # ranking_players = PhaseDayPlayersRankingSerializer(source='*')

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
        return PhaseDayRankingSerializer(context={'request': self.context['request']}).to_representation(
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
    permissions = DRYPermissionsField()
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
            return TeamDayScoreSerializer(many=True, read_only=True,
                                          context={'request': self.context['request']}).to_representation(
                league_models.TeamDayScore.objects.filter(day__in=days, team=obj).select_related('team',
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


class PlayersRankingSerializer(serializers.ModelSerializer):
    players_ranking = serializers.SerializerMethodField()
    phases = LeagueInstancePhaseSerializer(source="leagueinstancephase_set", many=True, read_only=True)

    @timed
    def get_players_ranking(self, obj):
        latest_day_by_phase = league_models.LeagueInstancePhase.objects.filter(league_instance=obj).annotate(
            latest_day=models.Max('leagueinstancephaseday__journee__numero'))
        score_by_id = dict()
        for phase in latest_day_by_phase:
            for tds in league_models.TeamDayScore.objects.filter(day__league_instance_phase=phase,
                                                                 day__journee__numero=phase.latest_day).select_related(
                'day__league_instance_phase'):
                if tds.attributes and 'composition' in tds.attributes:
                    for poste in ['G', 'D', 'M', 'A']:
                        for psco in tds.attributes['composition'][poste]:
                            if not psco['player']['id'] in score_by_id:
                                score_by_id.update({psco['player']['id']: dict({'scores': []})})
                            scoval = float('%.2f' % round(psco['score'] / psco['score_factor'], 2))
                            score_by_id[psco['player']['id']]['scores'].append(dict({'phase': phase.id,
                                                                                     'score': scoval}))
        # fetch players
        players = l1models.Joueur.objects.select_related('club').filter(
            pk__in=[key for key, _ in score_by_id.items()])
        return PlayerWithScoreSerializer(
            many=True, read_only=True,
            context={'request': self.context['request'], 'score_by_id': score_by_id}).to_representation(players)

    class Meta:
        model = league_models.LeagueInstance
        fields = ('phases', 'players_ranking',)


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


class SaleSerializer(SaleSummarySerializer):
    winner = serializers.SerializerMethodField()
    amount = serializers.SlugRelatedField(source='winning_auction', slug_field='value', read_only=True)
    auctions = serializers.SerializerMethodField()

    def get_auctions(self, obj):
        return AuctionSerializer(transfer_models.Auction.objects.filter(sale=obj).order_by('value'), read_only=True,
                                 many=True, context=self.context).data

    def get_winner(self, obj):
        if obj.winning_auction:
            return TeamHdrSerializer(obj.winning_auction.team, read_only=True, context=self.context).data
        return None

    class Meta:
        model = transfer_models.Sale
        fields = ('id', 'rank', 'type', 'player', 'author', 'min_price', 'winner', 'amount', 'auctions')


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


class PlayerMerkatoSerializer(PlayerHdrSerializer):
    current_signing = serializers.SerializerMethodField()
    current_sale = serializers.SerializerMethodField()


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
