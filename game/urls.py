from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from .admin_import import admin_import_site
from . import frontend

urlpatterns = [
    url(r'^rest/', include('game.rest.urls')),
    url(r'^home/info/$', frontend.HomePage.as_view(), name="home_info"),
    url(r'^home/result/rencontre/(?P<pk>[0-9]+)/$', frontend.ResultRencontreView.as_view(),
        name="result_rencontre-detail"),
    url(r'^home/result/club/(?P<pk>[0-9]+)/$', frontend.ClubView.as_view(),
        name="club-detail"),
    url(r'^home/stat/$', frontend.StatView.as_view(),
        name="stat-detail"),
    url(r'^home/stat/joueur/(?P<pk>[0-9]+)/$', frontend.StatJoueurView.as_view(),
        name="stat_joueur-detail"),
    url(r'^home/result/journee/latest/$', frontend.ResultJourneeView.as_view(),
        name="result_journee-latest"),
    url(r'^home/result/journee/(?P<pk>[0-9]+)/$', frontend.ResultJourneeView.as_view(),
        name="result_journee-detail"),

    url(r'^league/(?P<pk>[0-9]+)/wall/$', frontend.LeagueWallView.as_view(),
        name="league_wall-detail"),
    url(r'^league/(?P<pk>[0-9]+)/ekyp/$', frontend.LeagueEkypView.as_view(),
        name="league_ekyp-detail"),
    url(r'^league/(?P<pk>[0-9]+)/ekyp/(?P<team_pk>[0-9]+)$', frontend.LeagueEkypView.as_view(),
        name="league_team-detail"),
    url(r'^league/(?P<pk>[0-9]+)/ranking/$', frontend.LeagueRankingView.as_view(),
        name="league_ranking-detail"),
    url(r'^league/(?P<pk>[0-9]+)/merkatoresults/latest$', frontend.LeagueMerkatoResultsView.as_view(),
        name="league_merkatoresults-latest"),
    url(r'^league/(?P<pk>[0-9]+)/merkatoresults/(?P<session_pk>[0-9]+)$', frontend.LeagueMerkatoResultsView.as_view(),
        name="league_merkatoresults-session"),
    url(r'^import/', admin_import_site.urls, name='import'),
]
