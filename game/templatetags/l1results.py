__author__ = 'mgrandrie'
import operator
from django import template
from django.template import defaultfilters

from ligue1 import models as l1models


register = template.Library()


@register.inclusion_tag('game/tags/l1results_rencontre_score.html')
def rencontre_score(rencontre):
    if rencontre.resultat is None:
        score_dom = '?'
        score_ext = '?'
    else:
        score_dom = rencontre.resultat['dom']['buts_pour']
        score_ext = rencontre.resultat['ext']['buts_pour']
    return {'rid': rencontre.pk, 'club_dom': rencontre.club_domicile.nom, 'club_ext': rencontre.club_exterieur.nom,
            'score_dom':
                score_dom, 'score_ext': score_ext}


@register.inclusion_tag('game/tags/l1results_last_journees.html')
def last_journees(nb=1):
    """
    Retourne les résultats de la dernière journée enregistrée
    :param nb:
    :return:
    """
    journees = l1models.Journee.objects.order_by('-fin')[:nb]
    return {'journees': sorted(journees, key=operator.attrgetter('fin'))}


@register.filter()
def journee_dates(journee, pattern=None):
    if journee.debut == journee.fin:
        return defaultfilters.date(journee.debut, pattern)
    else:
        sep_char = '-'
        return '%s %s %s' % (defaultfilters.date(journee.debut, pattern), sep_char, defaultfilters.date(journee.fin,
                                                                                                        pattern))


@register.inclusion_tag('game/tags/l1results_rencontre_summary.html')
def rencontre_summary(rencontre, equipe):
    agglo = {}
    for perf in rencontre.performances.filter(details__equipe=equipe):
        for key in ['goals_scored', 'goals_assists', 'penalties_scored', 'penalties_awarded']:
            if perf.details['stats'][key] > 0:
                if key not in agglo:
                    agglo[key] = {}
                agglo[key][perf.joueur] = perf.details['stats'][key]
    return {'summary': agglo}


@register.filter()
def format_scorer(joueur, stat):
    if stat[joueur] == 1:
        return joueur.__str__()
    else:
        return joueur.__str__() + ' x%d' % stat[joueur]