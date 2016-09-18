from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _


class HomePage(TemplateView):
    template_name = 'kcup/game_base.html'
