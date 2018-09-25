from django.views.generic import ListView, FormView, DeleteView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.shortcuts import reverse, redirect
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

from game.forms import CreateTeamForm, JoinTeamForm
from game.models.league_models import Team
from game.models.invitation_models import TeamInvitation


class TeamListView(FormMixin, ListView):
    template_name = 'game/user/team_list.html'
    form_class = JoinTeamForm

    def get_queryset(self):
        return Team.objects.filter(managers__user=self.request.user).annotate(
            is_captain=Count(1, filter=Q(managers__is_team_captain=True)))

    context_object_name = 'teams'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamListView, self).get_context_data(*args, **kwargs)
        # team invitations
        context['team_invitations'] = TeamInvitation.objects.filter(team__managers__user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('user-teams-list')

    def form_valid(self, form):
        teaminvite = TeamInvitation.objects.get(code=form.data.get('code'))
        teaminvite.user = self.request.user
        teaminvite.save()
        return super(TeamListView, self).form_valid(form)


class TeamCreateView(FormView):
    template_name = 'game/user/team_creation.html'
    form_class = CreateTeamForm

    def get_success_url(self):
        return reverse('user-teams-list')

    def form_valid(self, form):
        Team.objects.create_for_user(name=form.data.get('name'), user=self.request.user)
        return super(TeamCreateView, self).form_valid(form)


class TeamInvitationView(DetailView):
    template_name = TeamListView.template_name

    def get_queryset(self):
        return Team.objects.filter(managers__user=self.request.user, managers__is_team_captain=True)

    def get(self, request, *args, **kwargs):
        # get existing invitation
        invite = TeamInvitation.objects.filter(team=self.get_object(), status='OPENED').first()
        if invite is None:
            TeamInvitation.objects.create(team=self.get_object())
        return redirect('user-teams-list')


class TeamDeleteView(DeleteView):
    model = Team
    success_url = reverse_lazy('user-teams-list')
    template_name = 'game/user/team_confirm_delete.html'

    def get_queryset(self):
        return Team.objects.filter(managers__user=self.request.user, managers__is_team_captain=True)

    def get_object(self, queryset=None):
        obj = super(TeamDeleteView, self).get_object(queryset)
        if obj.league is not None:
            raise PermissionDenied()
        return obj


class TeamInvitationAcceptView(DetailView):
    model = TeamInvitation
    success_url = reverse_lazy('user-teams-list')
    template_name = 'game/user/teaminvitation_confirm_accept.html'

    def get_queryset(self):
        return TeamInvitation.objects.filter(team__managers__user=self.request.user,
                                             team__managers__is_team_captain=True,
                                             user__isnull=False)

    def post(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.get_object().accept()
        return HttpResponseRedirect(success_url)
