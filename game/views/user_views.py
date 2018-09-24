from django.views.generic import TemplateView, ListView, FormView
from django.shortcuts import reverse
from django.db.models import Count, Q
from game.forms import CreateTeamForm
from game.models.league_models import Team


class TeamListView(ListView):
    template_name = 'game/user/team_list.html'

    def get_queryset(self):
        return Team.objects.filter(managers__user=self.request.user).annotate(
            is_captain=Count(1, filter=Q(managers__is_team_captain=True)))

    context_object_name = 'teams'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamListView, self).get_context_data(*args, **kwargs)
        return context


class TeamCreateView(FormView):
    template_name = 'game/user/team_creation.html'
    form_class = CreateTeamForm

    def get_success_url(self):
        return reverse('user-teams-list')

    def form_valid(self, form):
        Team.objects.create_for_user(name=form.data.get('name'), user=self.request.user)
        return super(TeamCreateView, self).form_valid(form)
