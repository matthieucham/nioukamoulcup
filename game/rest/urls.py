from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from game.rest import league

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^leagues/(?P<league_pk>[0-9]+)/ranking/current/$',
        league.LeagueInstanceRankingView.as_view(),
        name='leagueranking-current')
])