from django.db.models.query_utils import Q
from django.http import Http404
from django.utils.timezone import localtime, now
from django.db import models

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

from dry_rest_permissions.generics import DRYObjectPermissions

from game.models import league_models, transfer_models
from ligue1 import models as l1models
from game.rest import serializers
from utils.timer import timed


# TODO : Faire le ménage dans ces vues, ne garder que celles utilisées par le composant React


class CurrentLeagueInstanceMixin:
    def _get_current_league_instance(self, pk):
        return league_models.LeagueInstance.objects.get_current(league=pk)


class LeagueInstanceRankingView(generics.RetrieveAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.LeagueInstanceRankingSerializer
    lookup_field = "league__pk"

    def get_queryset(self):
        return league_models.LeagueInstance.objects.filter(current=True)

    def get_serializer_context(self):
        ctxt = super(LeagueInstanceRankingView, self).get_serializer_context()
        # ctxt['expand_attributes'] = True
        return ctxt


class TeamDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.TeamDetailSerializer
    queryset = league_models.Team.objects.all()
    permission_classes = (DRYObjectPermissions,)

    def get_serializer_context(self):
        return {"request": self.request, "current": True}  # TODO optim pour FSY


class ClubListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    serializer_class = serializers.ClubSerializer

    def get_queryset(self):
        league_pk = self.kwargs["league_pk"]
        instance = self._get_current_league_instance(league_pk)
        return l1models.Club.objects.filter(participations=instance.saison)


class TeamSigningsListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.SigningSerializer
    ordering_fields = ("begin",)
    ordering = ("begin",)

    def get_queryset(self):
        team = league_models.Team.objects.get(pk=self.kwargs["team_pk"])
        return league_models.Signing.objects.filter(
            team=team, league_instance=self._get_current_league_instance(team.league)
        ).order_by("begin")


class TeamBankAccountHistoryListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.BankAccountHistorySerializer
    ordering_fields = ("date",)
    ordering = ("date",)

    def get_queryset(self):
        team_pk = self.kwargs["team_pk"]
        return league_models.BankAccountHistory.objects.filter(
            bank_account__team=team_pk
        )


class TeamReleasesListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.ReleaseSerializer

    def get_queryset(self):
        team_pk = self.kwargs["team_pk"]
        return transfer_models.Release.objects.get_for_team(team_pk)


class TeamSalesListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.SaleSerializer

    def get_queryset(self):
        team_pk = self.kwargs["team_pk"]
        return transfer_models.Sale.objects.get_for_team(
            league_models.Team.objects.get(pk=team_pk)
        )


class LeagueResultsByJourneeListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.TeamDayCompoAndScoreSerializer

    def get_serializer_context(self):
        base_context = super(
            LeagueResultsByJourneeListView, self
        ).get_serializer_context()
        journee_numero = self.kwargs["journee_numero"]
        if int(journee_numero) == 0:
            base_context["current"] = True
        else:
            base_context["current"] = False
        return base_context

    def get_queryset(self):
        team_pk = self.kwargs["team_pk"]
        league_pk = self.kwargs["league_pk"]
        journee_numero = self.kwargs["journee_numero"]
        # numero special 0 pour le score "courant"

        days = league_models.LeagueInstancePhaseDay.objects.filter(
            league_instance_phase__league_instance=self._get_current_league_instance(
                league_pk
            )
        )
        if int(journee_numero) > 0:
            days = days.filter(journee__numero=journee_numero)

        qs = league_models.TeamDayScore.objects.filter(
            day__in=days, team=team_pk
        ).order_by("day__league_instance_phase")
        if int(journee_numero) == 0:
            qs = qs.filter(current=True)
        else:
            qs = qs.filter(current=False)
        return qs.order_by("day__league_instance_phase")


class NewPlayersRankingView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.NewPlayersRankingSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filter_fields = {"poste": ["exact"], "club": ["exact", "isnull"]}
    search_fields = (
        "nom",
        "surnom",
        "=prenom",
    )

    @timed
    def get_queryset(self):
        # limit to players which :
        # - are members of participating teams of the season of the current instance
        # - or have played at least one meeting in the season of the current instance
        # order by club then name
        instance = self._get_current_league_instance(self.kwargs["league_pk"])
        qs = (
            (
                l1models.Joueur.objects.filter(club__participations=instance.saison)
                | l1models.Joueur.objects.filter(
                    performances__rencontre__journee__saison=instance.saison
                )
            )
            .distinct()
            .order_by("club__nom", "nom")
        )
        return qs

    def get_players_score(self):
        league_pk = self.kwargs["league_pk"]
        instance = self._get_current_league_instance(league_pk)
        latest_day_by_phase = league_models.LeagueInstancePhase.objects.filter(
            league_instance=instance
        ).annotate(latest_day=models.Max("leagueinstancephaseday__journee__numero"))
        score_by_id = dict()
        for phase in latest_day_by_phase:
            for tds in league_models.TeamDayScore.objects.filter(
                day__league_instance_phase=phase, day__journee__numero=phase.latest_day
            ).select_related("day__league_instance_phase"):
                if tds.attributes and "composition" in tds.attributes:
                    for poste in ["G", "D", "M", "A"]:
                        for psco in tds.attributes["composition"][poste]:
                            if not psco["player"]["id"] in score_by_id:
                                score_by_id.update(
                                    {psco["player"]["id"]: dict({"scores": []})}
                                )
                            scoval = float(
                                "%.1f" % round(psco["score"] / psco["score_factor"], 1)
                            )
                            score_by_id[psco["player"]["id"]]["scores"].append(
                                dict({"phase": phase.id, "score": scoval})
                            )
        return score_by_id

    def get_phases(self):
        league_pk = self.kwargs["league_pk"]
        instance = self._get_current_league_instance(league_pk)
        return league_models.LeagueInstancePhase.objects.filter(
            league_instance=instance
        ).values("id", "name")

    @timed
    def get_serializer_context(self):
        base_context = super(NewPlayersRankingView, self).get_serializer_context()
        base_context["scoring_map"] = self.get_players_score()
        base_context["phases"] = self.get_phases()
        return base_context


class LeagueTeamInfoListView(generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.TeamInfoSerializer

    def get_queryset(self):
        league_pk = self.kwargs["pk"]
        qs = league_models.Team.objects.filter(league=league_pk)
        qs = self.get_serializer_class().setup_eager_loading(qs)
        return qs


class LeagueMerkatosListView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.MerkatoSerializer

    def get_queryset(self):
        return transfer_models.Merkato.objects.filter(
            league_instance=self._get_current_league_instance(self.kwargs["league_pk"])
        ).order_by("begin")


class MerkatoSessionView(CurrentLeagueInstanceMixin, generics.RetrieveAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.MerkatoSessionSerializer
    queryset = transfer_models.MerkatoSession.objects.filter(is_solved=True)


class DraftSessionView(CurrentLeagueInstanceMixin, generics.RetrieveAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.DraftSessionSerializer
    queryset = transfer_models.DraftSession.objects.filter(is_solved=True)


class PlayersForMerkatoView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.PlayerMerkatoSerializer
    pagination_class = PageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filter_fields = {"poste": ["exact"], "club": ["exact", "isnull"]}
    search_fields = (
        "nom",
        "surnom",
        "=prenom",
    )

    @timed
    def get_queryset(self):
        # limit to players which :
        # - are members of participating teams of the season of the current instance
        # - or have played at least one meeting in the season of the current instance
        # order by club then name
        instance = self._get_current_league_instance(self.kwargs["league_pk"])
        qs = (
            (
                l1models.Joueur.objects.filter(club__participations=instance.saison)
                | l1models.Joueur.objects.filter(
                    performances__rencontre__journee__saison=instance.saison
                )
            )
            .distinct()
            .order_by("club__nom", "nom")
        )
        return qs

    @timed
    def get_serializer_context(self):
        base_context = super(PlayersForMerkatoView, self).get_serializer_context()
        league_pk = self.kwargs["league_pk"]
        user = base_context.get("request").user
        team = (
            league_models.LeagueMembership.objects.filter(user=user, league=league_pk)
            .first()
            .team
        )
        base_context["signings_map"] = dict(
            league_models.Signing.objects.filter(
                team__division=team.division,
                end__isnull=True,
                league_instance=self._get_current_league_instance(league_pk),
            )
            .select_related("team")
            .values_list("player_id", "team__name")
        )
        base_context["sales_map"] = dict(
            transfer_models.Sale.objects.filter(merkato_session__is_solved=False)
            .filter(
                team__division=team.division,
                merkato_session__merkato__league_instance=self._get_current_league_instance(
                    league_pk
                ),
            )
            .select_related("team")
            .values_list("player_id", "team__name")
        )
        return base_context


class PlayersForDraftView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.PlayerMerkatoSerializer
    pagination_class = PageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filter_fields = {"poste": ["exact"], "club": ["exact", "isnull"]}
    search_fields = (
        "nom",
        "surnom",
        "=prenom",
    )

    @timed
    def get_queryset(self):
        # limit to players which :
        # - are members of participating teams of the season of the current instance
        # - or have played at least one meeting in the season of the current instance
        # - are not indraftable
        # order by club then name
        instance = self._get_current_league_instance(self.kwargs["league_pk"])
        qs = (
            (
                l1models.Joueur.objects.filter(club__participations=instance.saison)
                | l1models.Joueur.objects.filter(
                    performances__rencontre__journee__saison=instance.saison
                )
            )
            .filter(Q(indraftable__isnull=True) | Q(indraftable=False))
            .distinct()
            .order_by("club__nom", "nom")
        )
        return qs

    @timed
    def get_serializer_context(self):
        base_context = super(PlayersForDraftView, self).get_serializer_context()
        league_pk = self.kwargs["league_pk"]
        user = base_context.get("request").user
        team = (
            league_models.LeagueMembership.objects.filter(user=user, league=league_pk)
            .first()
            .team
        )
        base_context["signings_map"] = dict(
            league_models.Signing.objects.filter(
                team__division=team.division,
                end__isnull=True,
                league_instance=self._get_current_league_instance(league_pk),
            )
            .select_related("team")
            .values_list("player_id", "team__name")
        )
        base_context["sales_map"] = dict(
            transfer_models.Sale.objects.filter(merkato_session__is_solved=False)
            .filter(
                team__division=team.division,
                merkato_session__merkato__league_instance=self._get_current_league_instance(
                    league_pk
                ),
            )
            .select_related("team")
            .values_list("player_id", "team__name")
        )
        return base_context


class PlayersForMVView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.PlayerForMVSerializer
    pagination_class = PageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filter_fields = {"poste": ["exact"], "club": ["exact", "isnull"]}
    search_fields = (
        "nom",
        "surnom",
        "=prenom",
    )

    @timed
    def get_queryset(self):
        # limit to players which :
        # - are current signings of the team
        # order by club then name
        instance = self._get_current_league_instance(self.kwargs["league_pk"])
        team = league_models.Team.objects.get(
            league=self.kwargs["league_pk"], managers__user=self.request.user
        )
        qs = (
            (
                l1models.Joueur.objects.filter(
                    signing__team=team,
                    signing__begin__lt=now(),
                    signing__end__isnull=True,
                    signing__league_instance=instance,
                )
            )
            .distinct()
            .order_by("club__nom", "nom")
        )
        return qs

    @timed
    def get_serializer_context(self):
        base_context = super(PlayersForMVView, self).get_serializer_context()
        league_pk = self.kwargs["league_pk"]
        user = base_context.get("request").user
        team = (
            league_models.LeagueMembership.objects.filter(user=user, league=league_pk)
            .first()
            .team
        )
        base_context["sales_map"] = dict(
            transfer_models.Sale.objects.filter(merkato_session__is_solved=False)
            .filter(
                team__division=team.division,
                merkato_session__merkato__league_instance=self._get_current_league_instance(
                    league_pk
                ),
            )
            .select_related("team")
            .values_list("player_id", "team__name")
        )
        return base_context


class CurrentMerkatoView(CurrentLeagueInstanceMixin, generics.ListAPIView):
    permission_classes = (DRYObjectPermissions,)
    serializer_class = serializers.CurrentMerkatoSerializer

    def get_serializer_context(self):
        instance = self._get_current_league_instance(self.kwargs["league_pk"])
        return {
            "request": self.request,
            "team": league_models.LeagueMembership.objects.get(
                user=self.request.user, league=instance.league
            ).team,
        }

    def get_queryset(self):
        instance = self._get_current_league_instance(self.kwargs["league_pk"])
        league_models.LeagueMembership.objects.get(
            user=self.request.user, league=instance.league
        ).team
        return transfer_models.Merkato.objects.filter(
            league_instance=instance,
            begin__lte=localtime(now()),
            last_solving__gte=localtime(now()),
        ).order_by("begin")
