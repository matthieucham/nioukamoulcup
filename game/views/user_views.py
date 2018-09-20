from django.views.generic import TemplateView, ListView
from game.models.league_models import Team
from django.db.models import Count, Q


class TeamListView(ListView):
    template_name = 'game/user/team_list.html'

    def get_queryset(self):
        return Team.objects.filter(managers__user=self.request.user).annotate(
            is_captain=Count(1, filter=Q(managers__is_team_captain=True)))

    context_object_name = 'teams'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamListView, self).get_context_data(*args, **kwargs)
        return context
