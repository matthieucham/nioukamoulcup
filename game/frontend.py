from django.views.generic import TemplateView, DetailView
from django.utils.translation import ugettext_lazy as _

from ligue1 import models as l1models


class HomePage(TemplateView):
    template_name = 'game/home/info.html'


class ResultRencontreView(DetailView):
    model = l1models.Rencontre
    template_name = 'game/home/result_rencontre.html'