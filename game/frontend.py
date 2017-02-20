from django.views.generic import TemplateView, DetailView
# from chartit import DataPool, Chart
from graphos.sources.model import ModelDataSource, SimpleDataSource
from graphos.renderers.morris import AreaChart, LineChart

from . import models
from ligue1 import models as l1models


class HomePage(TemplateView):
    template_name = 'game/home/info.html'


class ResultRencontreView(DetailView):
    model = l1models.Rencontre
    template_name = 'game/home/result_rencontre.html'


class StatJoueurView(DetailView):
    model = l1models.Joueur
    template_name = 'game/home/stat_joueur.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StatJoueurView, self).get_context_data(**kwargs)
        # Step 1: Create a DataPool with the data we want to retrieve.
        saisonscoring = models.SaisonScoring.objects.filter(saison__est_courante__isnull=False)[0]
        jjscores = models.JJScore.objects.list_scores_for_joueur(joueur=self.object, saison_scoring=saisonscoring)
        data_source_array = [['J', 'Pts']]
        for jjs in jjscores:
            data_source_array.append([jjs.journee_scoring.journee.numero,
                                      round(float(jjs.note or 0) + float(jjs.compensation or 0) + float(jjs.bonus or 0),
                                            3)])
        data_source = SimpleDataSource(data_source_array)
        # data_source = ModelDataSource(models.JJScore.objects.list_scores_for_joueur(joueur=self.object,
        # saison_scoring=saisonscoring),
        #                               fields=['journee_scoring__journee__numero', 'note'])
        context['chart'] = AreaChart(data_source, width=580,
                                     options={'resize': True, 'hideHover': 'auto', 'parseTime': False,
                                              'fillOpacity': 0.6, 'ymax': 'auto 20', 'grid': False,
                                              'goals': [0.0, 5.0, 10.0, 15.0, 20.0]})
        #
        # scoredata = DataPool(series=
        # [{'options': {
        # 'source': models.JJScore.objects.list_scores_for_joueur(joueur=self.object,
        # saison_scoring=saisonscoring
        # )},
        # 'terms': [
        #                            'numero',
        #                            'points',
        #                            'bonus']}
        #                      ])
        # # Step 2: Create the Chart object
        # cht = Chart(datasource=scoredata,
        #             series_options=[{'options': {'type': 'line', 'stacking': False},
        #                              'terms': {
        #                                  'numero': [
        #                                      'points',
        #                                      'bonus']}}],
        #             chart_options={'title': {
        #                 'text': 'Points marqués par journée'},
        #                            'xAxis': {
        #                                'title': {
        #                                    'text': 'journee'}}})
        # # context['scores'] = models.JJScore.objects.filter(joueur=self.object).order_by(
        # # 'journee_scoring__journee__numero')
        # context['scorechart'] = cht
        return context


class LeagueWallView(DetailView):
    model = models.League
    template_name = 'game/league/wall.html'