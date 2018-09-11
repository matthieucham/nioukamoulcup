from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from .admin_import import admin_import_site
from .views import HomePage, ResultRencontreView, ClubView, StatView, StatJoueurView, ResultJourneeView, \
    LeagueEntryDetail, LeagueWallView, LeagueEkypView, LeagueRankingView, LeagueMerkatoResultsView, LeagueMerkatoView

home_urls = [
    url(r'^info/$', LeagueEntryDetail.as_view(), name="home_info"),
    url(r'^info/', include('zinnia.urls')),
    url(r'^result/rencontre/(?P<pk>[0-9]+)/$', ResultRencontreView.as_view(), name="result_rencontre-detail"),
    url(r'^result/club/(?P<pk>[0-9]+)/$', ClubView.as_view(), name="club-detail"),
    url(r'^stat/$', StatView.as_view(), name="stat-detail"),
    url(r'^stat/joueur/(?P<pk>[0-9]+)/$', StatJoueurView.as_view(), name="stat_joueur-detail"),
    url(r'^result/journee/latest/$', ResultJourneeView.as_view(), name="result_journee-latest"),
    url(r'^result/journee/(?P<pk>[0-9]+)/$', ResultJourneeView.as_view(), name="result_journee-detail"),
]

league_urls = [
    url(r'^wall/$', LeagueWallView.as_view(), name="league_wall-detail"),
    url(r'^ekyp/$', LeagueEkypView.as_view(), name="league_ekyp-detail"),
    url(r'^ekyp/(?P<team_pk>[0-9]+)$', LeagueEkypView.as_view(), name="league_team-detail"),
    url(r'^ranking/$', LeagueRankingView.as_view(), name="league_ranking-detail"),
    url(r'^merkato/$', LeagueMerkatoView.as_view(), name="league_merkato"),
    url(r'^merkatoresults/latest$', LeagueMerkatoResultsView.as_view(), name="league_merkatoresults-latest"),
    url(r'^merkatoresults/(?P<session_pk>[0-9]+)$', LeagueMerkatoResultsView.as_view(),
        name="league_merkatoresults-session"),
]

urlpatterns = [
    url(r'^rest/', include('game.rest.urls')),
    url(r'^home/', include(home_urls)),
    url(r'^league/(?P<pk>[0-9]+)/', include(league_urls)),
    url(r'^import/', admin_import_site.urls, name='import'),
]
