from django.views.generic import TemplateView, ListView
from game.models.league_models import Team


class TeamListView(ListView):

    template_name = 'game/user/team_list.html'

    def get_queryset(self):
        return Team.objects.filter(managers__user=self.request.user)

    context_object_name = 'teams'
