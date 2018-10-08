from django.views.generic import DetailView, FormView
from django.shortcuts import reverse
from rules.contrib.views import PermissionRequiredMixin
from game.models import League, LeagueInstance, LeagueInstancePhase, LeagueInstancePhaseDay, LeagueMembership, Team, \
    MerkatoSession, Merkato, Sale, Auction
from ligue1.models import Joueur
from django.utils.timezone import localtime, now
from django.db.models import Count
from game.rest.redux_state import StateInitializerMixin
from game.rest import serializers
from game.forms import RegisterPaForm, RegisterMvForm, RegisterOffersForm
from decimal import Decimal


class BaseLeagueView(PermissionRequiredMixin, DetailView):
    model = League
    template_name = 'game/league/league_base.html'
    permission_required = 'game.view_league'
    component = 'test'

    def get_current_league_instance(self):
        return LeagueInstance.objects.get_current(league=self.get_object())

    def get_my_team(self):
        return LeagueMembership.objects.get(user=self.request.user, league=self.get_object()).team

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        # Call the base implementation first to get a context
        context = super(BaseLeagueView, self).get_context_data(**kwargs)
        context['team'] = self.get_my_team()
        context['instance'] = self.get_current_league_instance()
        context['component'] = self.component
        return context


class LeagueWallView(StateInitializerMixin, BaseLeagueView):
    template_name = 'game/league/wall.html'
    component = 'test'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueWallView, self).get_context_data(**kwargs)
        serializer = serializers.LeagueInstancePhaseDaySerializer(
            LeagueInstancePhaseDay.objects.get_latest_day_for_phases(
                LeagueInstancePhase.objects.filter(league_instance=context.get('instance'))), many=True,
            context={'request': self.request})
        # context['PRELOADED_STATE'] = {
        #     'ranking': []  # json.loads(str(JSONRenderer().render(serializer.data), 'utf-8'))
        # }

        context['PRELOADED_STATE'] = self.init_common(self.request, self.object.pk)
        return context


class LeagueEkypView(StateInitializerMixin, BaseLeagueView):
    template_name = 'game/league/ekyp.html'
    component = 'ekyp'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueEkypView, self).get_context_data(**kwargs)

        if 'team_pk' in self.kwargs and self.kwargs['team_pk'] != context.get('team').pk:
            context['component'] = 'team'
            context['PRELOADED_STATE'] = self.init_from_team(self.request,
                                                             Team.objects.filter(
                                                                 managers__league=self.kwargs['pk']).distinct().get(
                                                                 pk=self.kwargs['team_pk']))
        else:
            context['PRELOADED_STATE'] = self.init_from_team(self.request, context.get('team'))
        return context


class LeagueRankingView(StateInitializerMixin, BaseLeagueView):
    component = 'league'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueRankingView, self).get_context_data(**kwargs)
        context['PRELOADED_STATE'] = self.init_from_league(self.request, self.object)
        return context


class BaseMerkatoSessionsListView(StateInitializerMixin, BaseLeagueView):

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BaseMerkatoSessionsListView, self).get_context_data(**kwargs)
        context['sessions'] = MerkatoSession.objects.filter(
            merkato__league_instance=self.get_current_league_instance(), is_solved=True).order_by(
            '-solving')
        return context


class LeagueMerkatoResultsView(BaseMerkatoSessionsListView):
    template_name = 'game/league/merkato_results.html'
    component = 'merkatoresults'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueMerkatoResultsView, self).get_context_data(**kwargs)
        if 'session_pk' in self.kwargs:
            msession = MerkatoSession.objects.get(
                merkato__league_instance=self.get_current_league_instance(), is_solved=True,
                pk=self.kwargs['session_pk'])
            context['PRELOADED_STATE'] = self.init_from_merkatosession(self.request, msession)
        else:
            # latest
            context['PRELOADED_STATE'] = self.init_from_merkatosession(self.request, context['sessions'].first())
        return context


class LeagueMerkatoView(FormView, BaseMerkatoSessionsListView):
    template_name = 'game/league/merkato.html'
    component = 'merkato'
    form_class = RegisterOffersForm

    def get_context_data(self, **kwargs):
        context = super(LeagueMerkatoView, self).get_context_data(**kwargs)
        merkatos = Merkato.objects.filter(league_instance=context['instance'], end__gt=localtime(now())).order_by(
            'begin')
        context['PRELOADED_STATE'] = self.init_current_merkatos(self.request, context['team'], merkatos)
        return context

    def get_merkato(self):
        if 'merkato_pk' in self.kwargs:
            return Merkato.objects.get(pk=self.kwargs['merkato_pk'])
        return None

    def get_form_kwargs(self):
        kw = super(LeagueMerkatoView, self).get_form_kwargs()
        sessions = MerkatoSession.objects.filter(
            merkato__in=Merkato.objects.filter(league_instance=self.get_current_league_instance(),
                                               end__gt=localtime(now())), is_solved=False,
            solving__gt=localtime(now())).annotate(
            num_sales=Count('sale')).filter(num_sales__gt=0)
        sales = []
        for ms in sessions:
            sales.extend(ms.sale_set.all())
        kw['sales'] = sales
        kw['team'] = self.get_my_team()
        kw['merkato'] = self.get_merkato()
        return kw

    def get_success_url(self):
        return reverse('league_merkato', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        # create or update Auctions
        for field, val in form.cleaned_data.items():
            if field.startswith('_offer_for_sale__'):
                spk = int(field[len('_offer_for_sale__'):])
                if val:
                    Auction.objects.update_or_create(
                        sale=Sale.objects.get(pk=spk),
                        team=self.get_my_team(),
                        defaults={'value': val}
                    )
                else:
                    Auction.objects.filter(
                        sale=Sale.objects.get(pk=spk),
                        team=self.get_my_team()).delete()
        return super(LeagueMerkatoView, self).form_valid(form)


class LeagueRegisterPAView(FormView, BaseLeagueView):
    template_name = 'game/league/merkato.html'
    form_class = RegisterPaForm

    def get_merkato(self):
        return Merkato.objects.get(pk=self.kwargs['merkato_pk'])

    def get_form_kwargs(self):
        kw = super(LeagueRegisterPAView, self).get_form_kwargs()
        kw['team'] = self.get_my_team()
        kw['merkato'] = self.get_merkato()
        return kw

    def get_success_url(self):
        return reverse('league_merkato', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        # create Sale
        Sale.objects.create(
            player=Joueur.objects.get(pk=form.cleaned_data.get('picked_id')),
            team=self.get_my_team(),
            merkato_session=MerkatoSession.objects.get_next_available(self.get_merkato()),
            min_price=form.cleaned_data.get('amount'),
            type='PA'
        )
        return super(LeagueRegisterPAView, self).form_valid(form)


class LeagueRegisterMVView(FormView, BaseLeagueView):
    template_name = 'game/league/merkato.html'
    form_class = RegisterMvForm

    def get_merkato(self):
        return Merkato.objects.get(pk=self.kwargs['merkato_pk'])

    def get_form_kwargs(self):
        kw = super(LeagueRegisterMVView, self).get_form_kwargs()
        kw['team'] = self.get_my_team()
        kw['merkato'] = self.get_merkato()
        return kw

    def get_success_url(self):
        return reverse('league_merkato', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        # create Sale
        Sale.objects.create(
            player=Joueur.objects.get(pk=form.cleaned_data.get('picked_id')),
            team=self.get_my_team(),
            merkato_session=MerkatoSession.objects.get_next_available(self.get_merkato()),
            min_price=form.cleaned_data.get('amount'),
            type='MV'
        )
        return super(LeagueRegisterMVView, self).form_valid(form)
