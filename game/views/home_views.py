from django.views.generic import TemplateView, DetailView
from django.utils import timezone
from django.db.models import Q, F, Case, When, NullBooleanField
from graphos.sources.model import SimpleDataSource
from graphos.renderers.morris import AreaChart
# from graphos.renderers.gchart import AreaChart
from ligue1 import models as l1models
from game.models import SaisonScoring, JJScore, SJScore
from game.forms import StatsForm, PositionForm


class LandingPage(TemplateView):
    template_name = 'game/landing.html'


class MentionsPage(TemplateView):
    template_name = 'game/mentions.html'


class HomePage(TemplateView):
    template_name = 'game/home/info.html'


class ResultRencontreView(DetailView):
    model = l1models.Rencontre
    template_name = 'game/home/result_rencontre.html'


class ClubView(DetailView):
    model = l1models.Club
    template_name = 'game/home/club_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClubView, self).get_context_data(**kwargs)
        saisonscoring = SaisonScoring.objects.filter(saison__est_courante__isnull=False).first()
        context['players'] = []
        deco_joueurs = self.object.joueurs.filter(sjscore__saison_scoring=saisonscoring).annotate(
            nb_notes=F('sjscore__nb_notes')).annotate(avg_note=F('sjscore__avg_note')).annotate(
            bonuses=F('sjscore__details')).order_by('nom')
        context['players'] = l1models.Joueur.objects.order_queryset_by_poste(deco_joueurs)
        rencontres = l1models.Rencontre.objects.select_related('club_domicile').select_related(
            'club_exterieur').select_related(
            'journee').filter(journee__saison__saisonscoring=saisonscoring).filter(
            Q(club_domicile=self.object) | Q(club_exterieur=self.object)).order_by('date')
        renc = list(rencontres.all())
        for r in renc:
            if r.club_domicile.pk == self.object.pk:
                setattr(r, 'diff', r.resultat['dom']['buts_pour'] - r.resultat['ext']['buts_pour'])
            else:
                setattr(r, 'diff', r.resultat['ext']['buts_pour'] - r.resultat['dom']['buts_pour'])
        context['rencontres'] = renc
        return context


class StatJoueurView(DetailView):
    model = l1models.Joueur
    template_name = 'game/home/stat_joueur.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StatJoueurView, self).get_context_data(**kwargs)
        # Step 1: Create a DataPool with the data we want to retrieve.
        saisonscoring = SaisonScoring.objects.filter(saison__est_courante__isnull=False).first()
        jjscores = JJScore.objects.list_scores_for_joueur(joueur=self.object,
                                                          saison_scoring=saisonscoring) \
            .select_related('rencontre__club_domicile') \
            .select_related('rencontre__club_exterieur').select_related('journee_scoring__journee')
        context['stats'] = SJScore.objects.filter(saison_scoring=saisonscoring, joueur=self.object).first()
        context['jjscores'] = jjscores
        data_source_array = [['J', 'Note', 'Bonus']]
        for jjs in jjscores:
            data_source_array.append([jjs.journee_scoring.journee.numero,
                                      round(float(jjs.note or 0) + float(jjs.compensation or 0), 3),
                                      float(jjs.bonus or 0)])
        data_source = SimpleDataSource(data_source_array)
        context['chart'] = AreaChart(data_source,
                                     # width=580,
                                     options={'resize': True,
                                              'hideHover': 'auto',
                                              'parseTime': False,
                                              'fillOpacity': 0.6,
                                              'ymin': 0,
                                              'ymax': 'auto 15',
                                              'grid': False,
                                              'behaveLikeLine': False,
                                              'goals': [0.0, 5.0, 10.0, 15.0, 20.0, 25.0]}
                                     # options={
                                     #     'title': self.object.display_name(),
                                     #     'isStacked': True,
                                     #     'legend': {'position': 'top', 'maxLines': 3},
                                     #     'hAxis': {'title': 'Journée'},
                                     #     'vAxis': {'title': 'Points', 'minValue': 0, 'ticks': [5, 10, 15, 20]},
                                     #     'chartArea': {'left': 'auto', 'top': 'auto', 'width': '80%', 'height': '80%'},
                                     #     'crosshair': {'trigger': 'both'},
                                     #     'curveType': 'function',
                                     #     'focusTarget': 'category',
                                     #     'pointSize': 5,
                                     # }
                                     )
        # historique
        context['past_seasons'] = SJScore.objects.exclude(saison_scoring=saisonscoring).filter(
            joueur=self.object).annotate(trust_leader=(
                Case(When(saison_scoring__saison__fin__gt=timezone.datetime(2016, 7, 1), then=True),
                        output_field=NullBooleanField()))).order_by('-saison_scoring__saison__fin')

        return context


def compute_team(selection, best=True, criteria='note'):
    # test 5-3-2, 4-4-2, 3-5-2, 4-3-3
    formations = {
        '532': (1, 5, 3, 2),
        '442': (1, 4, 4, 2),
        '352': (1, 3, 5, 2),
        '433': (1, 4, 3, 3)
    }
    scores = dict()
    for name, (ng, nd, nm, na) in formations.items():
        scores[sum([getattr(jjs, criteria) for jjs in selection['G'][:ng]]) + sum(
            [getattr(jjs, criteria) for jjs in selection['D'][:nd]]) + sum(
            [getattr(jjs, criteria) for jjs in selection['M'][:nm]]) + sum(
            [getattr(jjs, criteria) for jjs in selection['A'][:na]])] = name
    if best:
        formation = scores[max(scores)]
    else:
        # worst
        formation = scores[min(scores)]
    team = list()
    team.append(selection['G'][:formations[formation][0]])
    team.append(selection['D'][:formations[formation][1]])
    team.append(selection['M'][:formations[formation][2]])
    team.append(selection['A'][:formations[formation][3]])
    return team


class ResultJourneeView(DetailView):
    model = l1models.Journee
    template_name = 'game/home/result_journee.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is None:
            # retrieve latest journee
            return l1models.Journee.objects.filter(saison__est_courante__isnull=False).order_by('-fin').first()
        else:
            return super(ResultJourneeView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ResultJourneeView, self).get_context_data(**kwargs)
        # Best of / worst of journee
        selection = {
            'best': {
                'G': [],
                'D': [],
                'M': [],
                'A': [],
            },
            'bonuses': {
                'G': [],
                'D': [],
                'M': [],
                'A': [],
            },
            'worst': {
                'G': [],
                'D': [],
                'M': [],
                'A': [],
            }
        }
        for p, nb in [('G', 1), ('D', 5), ('M', 5), ('A', 3)]:
            selection['best'][p].extend(
                JJScore.objects.get_n_best_or_worst(nb, self.object.saison, journee=self.object, poste=p))
            selection['bonuses'][p].extend(
                JJScore.objects.get_n_best_bonuses(nb, self.object.saison, journee=self.object, poste=p))
            selection['worst'][p].extend(
                JJScore.objects.get_n_best_or_worst(nb, self.object.saison, journee=self.object, poste=p,
                                                    best=False))

        context['best'] = compute_team(selection['best'])
        context['bonuses'] = compute_team(selection['bonuses'], criteria='bonus')
        context['worst'] = compute_team(selection['worst'], False)
        return context


class StatView(DetailView):
    model = l1models.Saison
    template_name = 'game/home/stat_saison.html'

    def get_object(self, queryset=None):
        scourante = l1models.SaisonCourante.objects.first()
        if scourante is not None:
            return scourante.saison
        return None

    def get_context_data(self, **kwargs):
        context = super(StatView, self).get_context_data(**kwargs)
        # Best of / worst of saison
        selection = {
            'best': {
                'G': [],
                'D': [],
                'M': [],
                'A': [],
            },
            'bonuses': {
                'G': [],
                'D': [],
                'M': [],
                'A': [],
            },
            'worst': {
                'G': [],
                'D': [],
                'M': [],
                'A': [],
            }
        }
        nb_notes_min = self.request.GET.get('nb_notes') or 1
        for p, nb in [('G', 1), ('D', 5), ('M', 5), ('A', 3)]:
            selection['best'][p].extend(
                SJScore.objects.get_n_best_or_worst(self.object, nb, p, nb_notes_min=nb_notes_min))
            selection['bonuses'][p].extend(
                SJScore.objects.get_n_best_bonuses(self.object, nb, p))
            selection['worst'][p].extend(
                SJScore.objects.get_n_best_or_worst(self.object, nb, p, False, nb_notes_min=nb_notes_min))

        context['stats_form'] = StatsForm(self.request.GET, saison=self.object) if self.request.GET.get(
            'nb_notes') else StatsForm(saison=self.object)
        context['position_form'] = PositionForm(self.request.GET) if self.request.GET.get(
            'position') else PositionForm()
        context['bestofall'] = JJScore.objects.get_n_best_or_worst(3, self.object, poste=self.request.GET.get(
            'position') or None)
        context['worstofall'] = JJScore.objects.get_n_best_or_worst(3, self.object, best=False,
                                                                    poste=self.request.GET.get(
                                                                        'position') or None)
        context['best'] = compute_team(selection['best'], criteria='avg_note')
        context['bonuses'] = compute_team(selection['bonuses'], criteria='total_bonuses')
        context['worst'] = compute_team(selection['worst'], False, criteria='avg_note')
        return context
