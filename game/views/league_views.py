from django.views.generic import DetailView, FormView
from django.shortcuts import reverse
from django.contrib import messages
from rules.contrib.views import PermissionRequiredMixin
from game.models import League, LeagueInstance, LeagueMembership, Team, \
    MerkatoSession, Merkato, Sale, Auction, DraftSession, DraftSessionRank, DraftPick, Signing, Release
from ligue1.models import Joueur
from django.utils.timezone import localtime, now
from django.db.models import Count
from game.rest.redux_state import StateInitializerMixin
from game.forms import RegisterPaForm, RegisterMvForm, RegisterOffersForm, RegisterDraftChoicesForm, RegisterCoverForm, ReleaseSigningForm
from django.http import HttpResponseRedirect
from .ensure_csrf_cookie_mixin import EnsureCsrfCookieMixin
from django.db import transaction


class BaseLeagueView(EnsureCsrfCookieMixin, PermissionRequiredMixin, DetailView):
    model = League
    template_name = 'game/league/league_react_base.html'
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

    def form_invalid(self, form):
        """If the form is invalid, redirect to the supplied URL. \
        (hack parce que les erreurs ne sont pas visible de toute façon)"""
        for key, errorlist in form.errors.items():
            for err in errorlist:
                messages.add_message(self.request, messages.ERROR, err)
        return HttpResponseRedirect(self.get_success_url())


class LeagueWallView(StateInitializerMixin, BaseLeagueView):
    template_name = 'game/league/wall.html'
    component = 'test'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueWallView, self).get_context_data(**kwargs)
        # context['PRELOADED_STATE'] = self.init_common(self.request, self.object.pk)
        context['next_merkato'] = Merkato.objects.filter(league_instance=context['instance'],
                                                         mode='BID',
                                                         end__gt=localtime(now())).order_by('begin').first()
        context['next_draft'] = Merkato.objects.filter(league_instance=context['instance'],
                                                       mode='DRFT',
                                                       end__gt=localtime(now())).order_by('begin').first()
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
        context['draftsessions'] = DraftSession.objects.filter(
            merkato__league_instance=self.get_current_league_instance(), is_solved=True).order_by(
            '-closing')
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


class LeagueDraftResultsView(BaseMerkatoSessionsListView):
    template_name = 'game/league/merkato_results.html'
    component = 'draftresults'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LeagueDraftResultsView, self).get_context_data(**kwargs)
        dsession = DraftSession.objects.get(
            merkato__league_instance=self.get_current_league_instance(), is_solved=True,
            pk=self.kwargs['session_pk'])
        context['PRELOADED_STATE'] = self.init_from_draftsession(self.request, dsession)
        return context


class LeagueMerkatoView(FormView, BaseMerkatoSessionsListView):
    template_name = 'game/league/merkato.html'
    component = 'merkato'
    form_class = RegisterOffersForm

    def get_context_data(self, **kwargs):
        context = super(LeagueMerkatoView, self).get_context_data(**kwargs)
        merkatos = Merkato.objects.filter(league_instance=context['instance'], begin__lte=localtime(now()),
                                          end__gt=localtime(now())).order_by(
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

    @transaction.atomic
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
        messages.add_message(self.request, messages.SUCCESS, 'Offres enregistrées')
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
        messages.add_message(self.request, messages.SUCCESS, 'PA enregistrée')
        return super(LeagueRegisterPAView, self).form_valid(form)


class LeagueEkypRegisterCoverView(FormView, BaseLeagueView):
    template_name = 'game/league/ekyp.html'
    form_class = RegisterCoverForm

    def get_success_url(self):
        return reverse('league_ekyp-detail', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        # update cover of "my_team" with form value
        team = self.get_my_team()
        try:
            team.attributes['perso']['cover'] = form.cleaned_data.get('cover_url')
        except KeyError:
            team.attributes['perso'] = {'cover': form.cleaned_data.get('cover_url')}
        team.save()
        messages.add_message(self.request, messages.SUCCESS, 'Image enregistrée')
        return super(LeagueEkypRegisterCoverView, self).form_valid(form)


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
        messages.add_message(self.request, messages.SUCCESS, 'MV enregistrée')
        return super(LeagueRegisterMVView, self).form_valid(form)


class LeagueRegisterDraftView(FormView, BaseLeagueView):
    template_name = 'game/league/merkato.html'
    form_class = RegisterDraftChoicesForm

    def get_draft_session(self):
        return DraftSession.objects.get(pk=self.kwargs['draftsession_pk'])

    def get_form_kwargs(self):
        kw = super(LeagueRegisterDraftView, self).get_form_kwargs()
        kw['team'] = self.get_my_team()
        kw['draft_session'] = self.get_draft_session()
        return kw

    def get_success_url(self):
        return reverse('league_merkato', kwargs={'pk': self.get_object().pk})

    @transaction.atomic
    def form_valid(self, form):
        # delete and recreate choices
        DraftPick.objects.filter(draft_session_rank__team=self.get_my_team(),
                                 draft_session_rank__signing__isnull=True).delete()
        for field, val in form.cleaned_data.items():
            if field.startswith('_pick_for_rank__') and val > 0:
                rank = int(field[len('_pick_for_rank__'):])
                DraftPick.objects.create(
                    pick_order=rank,
                    player=Joueur.objects.get(pk=val),
                    draft_session_rank=DraftSessionRank.objects.get(draft_session=self.get_draft_session(),
                                                                    team=self.get_my_team())
                )
        messages.add_message(self.request, messages.SUCCESS, 'Choix de draft enregistrés')
        return super(LeagueRegisterDraftView, self).form_valid(form)


class LeagueReleaseSigningView(FormView, BaseLeagueView):
    template_name = 'game/league/ekyp.html'
    form_class = ReleaseSigningForm

    def get_form_kwargs(self):
        kw = super(LeagueReleaseSigningView, self).get_form_kwargs()
        kw['team'] = self.get_my_team()
        kw['signing'] = Signing.objects.get(pk=self.kwargs['signing_pk'])
        kw['request'] = self.request
        return kw

    def get_success_url(self):
        return reverse('league_ekyp-detail', kwargs={'pk': self.get_object().pk})

    @transaction.atomic
    def form_valid(self, form):
        signing = Signing.objects.get(pk=self.kwargs['signing_pk'])
        Signing.objects.ending(signing)
        merkato = Merkato.objects.find_current_open_merkato_for_release(self.get_my_team())
        session = MerkatoSession.objects.get_next_available(merkato, dont_check_sales_count=True)

        Release.objects.create(signing=signing,
                               merkato_session=session,
                               amount=signing.attributes.get('release_amount'))

        messages.add_message(self.request, messages.SUCCESS, 'Revente enregistrée')
        return super(LeagueReleaseSigningView, self).form_valid(form)

