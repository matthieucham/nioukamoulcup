from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from game.rest import league

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^leagues/(?P<league_pk>[0-9]+)/ranking/$',
        league.LeagueInstanceRankingView.as_view(),
        name='leagueranking-current'),
    url(r'^teams/(?P<pk>[0-9]+)/$',
        league.TeamDetailView.as_view(),
        name='team-detail'),
    url(r'^leagues/(?P<league_pk>[0-9]+)/clubs$',
        league.ClubListView.as_view(),
        name='team-detail'),
])