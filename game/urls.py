from django.conf.urls import url

from . import frontend


urlpatterns = [
    url(r'^home/info/$', frontend.HomePage.as_view(), name="home_info"),
    url(r'^home/result/rencontre/(?P<pk>[0-9]+)/$', frontend.ResultRencontreView.as_view(),
        name="result_rencontre-detail"),
]