from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from game.rest import league, apiroot_view

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^$', apiroot_view.api_root, name='api-root'),
    url(r'^leagues/(?P<pk>[0-9]+)/ranking$',
        league.LeagueInstanceRankingView.as_view(),
        name='leagueranking-current'),
    url(r'^leagues/(?P<pk>[0-9]+)/teaminfos$',
        league.LeagueTeamInfoListView.as_view(),
        name='league-teaminfos'),
    url(r'^leagues/(?P<league_pk>[0-9]+)/journees/(?P<journee_numero>[0-9]+)/teams/(?P<team_pk>[0-9]+)$',
        league.LeagueResultsByJourneeListView.as_view(),
        name='league-journeeteam'),
    url(r'^leagues/(?P<league>[0-9]+)/players$',
        league.LeaguePlayersRankingView.as_view(),
        name='league-journeeteam'),
    url(r'^leagues/(?P<league_pk>[0-9]+)/merkatos$',
        league.LeagueMerkatosListView.as_view(),
        name='league_merkatos-list'),
    url(r'^leagues/(?P<league_pk>[0-9]+)/playersformerkato$',
        league.PlayersForMerkatoView.as_view(),
        name='playersformerkato-list'),
    url(r'^leagues/(?P<league_pk>[0-9]+)/currentmerkato$',
        league.CurrentMerkatoView.as_view(),
        name='openmerkatosessions-list'),
    url(r'^merkatosessions/(?P<pk>[0-9]+)$',
        league.MerkatoSessionView.as_view(),
        name='merkatosession-detail'),
    url(r'^teams/(?P<pk>[0-9]+)/$',
        league.TeamDetailView.as_view(),
        name='team-detail'),
    url(r'^leagues/(?P<league_pk>[0-9]+)/clubs$',
        league.ClubListView.as_view(),
        name='team-detail'),
    url(r'^teams/(?P<team_pk>[0-9]+)/signings$',
        league.TeamSigningsListView.as_view(),
        name='team-signings'),
    url(r'^teams/(?P<team_pk>[0-9]+)/bankaccounthistory$',
        league.TeamBankAccountHistoryListView.as_view(),
        name='team-bankaccounthistory'),
    url(r'^teams/(?P<team_pk>[0-9]+)/releases$',
        league.TeamReleasesListView.as_view(),
        name='team-releases'),
    url(r'^teams/(?P<team_pk>[0-9]+)/sales$',
        league.TeamSalesListView.as_view(),
        name='team-sales'),
])