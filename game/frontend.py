from django.views.generic import TemplateView, DetailView
from chartit import DataPool, Chart

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
        scoredata = DataPool(series=
                             [{'options': {
                                 'source': models.JJScore.objects.filter(joueur=self.object).order_by(
                                     'journee_scoring__saison_scoring__saison__debut',
                                     'journee_scoring__journee__numero')},
                               'terms': [
                                   'journee_scoring__journee__numero',
                                   'note',
                                   'compensation',
                                   'bonus']}
                              ])
        # Step 2: Create the Chart object
        cht = Chart(datasource=scoredata,
                    series_options=[{'options': {'type': 'line', 'stacking': False},
                                     'terms': {
                                         'journee_scoring__journee__numero': [
                                             'note',
                                             'compensation',
                                             'bonus']}}],
                    chart_options={'title': {
                        'text': 'Points marqués par journée'},
                                   'xAxis': {
                                       'title': {
                                           'text': 'journee'}}})
        context['scores'] = models.JJScore.objects.filter(joueur=self.object).order_by(
            'journee_scoring__journee__numero')
        context['scorechart'] = cht
        return context