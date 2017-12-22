from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import frontend


urlpatterns = [
    url(r'^rest/', include('game.rest.urls')),
    url(r'^home/info/$', frontend.HomePage.as_view(), name="home_info"),
    url(r'^home/result/rencontre/(?P<pk>[0-9]+)/$', frontend.ResultRencontreView.as_view(),
        name="result_rencontre-detail"),
    url(r'^home/stat/joueur/(?P<pk>[0-9]+)/$', frontend.StatJoueurView.as_view(),
        name="stat_joueur-detail"),

    url(r'^league/wall/(?P<pk>[0-9]+)/$', frontend.LeagueWallView.as_view(),
        name="league_wall-detail"),
    url(r'^league/ekyp/(?P<pk>[0-9]+)/$', frontend.LeagueEkypView.as_view(),
        name="league_ekyp-detail"),
    url(r'^league/ranking/(?P<pk>[0-9]+)/$', frontend.LeagueRankingView.as_view(),
        name="league_ranking-detail"),
]
