from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from game.rest import league, apiroot_view

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^$', apiroot_view.api_root, name='api-root'),
    url(r'^leagues/(?P<league_pk>[0-9]+)/ranking/$',
        league.LeagueInstanceRankingView.as_view(),
        name='leagueranking-current'),
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
    url(r'^teams/(?P<team_pk>[0-9]+)/releases',
        league.TeamReleasesListView.as_view(),
        name='team-releases'),
    url(r'^teams/(?P<team_pk>[0-9]+)/sales',
        league.TeamSalesListView.as_view(),
        name='team-sales'),
    url(r'^leagues/(?P<league_pk>[0-9]+)/journees/(?P<journee_numero>[0-9]+)/teams/(?P<team_pk>[0-9]+)$',
        league.LeagueResultsByJourneeListView.as_view(),
        name='league-journeeteam'),
])