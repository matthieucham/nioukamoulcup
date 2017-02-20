from django.conf.urls import url

from . import frontend


urlpatterns = [
    url(r'^home/info/$', frontend.HomePage.as_view(), name="home_info"),
    url(r'^home/result/rencontre/(?P<pk>[0-9]+)/$', frontend.ResultRencontreView.as_view(),
        name="result_rencontre-detail"),
    url(r'^home/stat/joueur/(?P<pk>[0-9]+)/$', frontend.StatJoueurView.as_view(),
        name="stat_joueur-detail"),

    url(r'^league/wall/(?P<pk>[0-9]+)/$', frontend.LeagueWallView.as_view(),
        name="league_wall"),
]