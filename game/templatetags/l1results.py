__author__ = 'mgrandrie'
import operator
from django import template
from django.template import defaultfilters

from ligue1 import models as l1models
from game import services

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


def sort_position_function(joueur):
    sort_order = {'G': 0, 'D': 1, 'M': 2, 'A': 3, None: 10}
    return sort_order[joueur.poste]


@register.inclusion_tag('game/tags/l1results_club_logo.html')
def club_logo(club, size='medium'):
    mapping = {'small': 32, 'medium': 48, 'big': 64, 'biggest': 128}
    return {'svg': club.maillot_svg, 'stroke': club.maillot_color_stroke, 'fill': club.maillot_color_bg,
            'size': mapping.get(size, mapping.get('medium'))}


@register.inclusion_tag('game/tags/l1results_team_players.html')
def joueurs_club(club):
    """
    Retourne la liste des joueurs de ce club
    :param club:
    :return:
    """
    joueurs = l1models.Joueur.objects.filter(club=club).order_by('nom')
    return {'team': club, 'players': sorted(joueurs, key=sort_position_function)}


@register.filter()
def journee_dates(journee, pattern=None):
    if journee.debut == journee.fin:
        return defaultfilters.date(journee.debut, pattern)
    else:
        sep_char = '-'
        return '%s %s %s' % (defaultfilters.date(journee.debut, pattern), sep_char, defaultfilters.date(journee.fin,
                                                                                                        pattern))


@register.inclusion_tag('game/tags/l1results_rencontre_summary.html')
def rencontre_summary(rencontre):
    agglo = {}
    for perf in rencontre.performances.all():
        for key in ['goals_scored', 'goals_assists', 'penalties_scored', 'penalties_awarded']:
            if perf.details['stats'][key] > 0:
                if key not in agglo:
                    agglo[key] = {'dom': {}, 'ext': {}}
                agglo[key][perf.details['equipe']][perf.joueur] = perf.details['stats'][key]
    return \
        {
            'summary': agglo,
            'header': {
                'dom': rencontre.club_domicile.nom,
                'ext': rencontre.club_exterieur.nom,
                'score_dom': rencontre.resultat['dom']['buts_pour'],
                'score_ext': rencontre.resultat['ext']['buts_pour']}
        }


@register.inclusion_tag('game/tags/l1results_rencontre_team.html')
def rencontre_team(rencontre, equipe):
    out = {'G': [], 'D': [], 'M': [], 'A': []}
    for perf in rencontre.performances.filter(details__equipe=equipe):
        base_stats = {'time': perf.temps_de_jeu,
                      'rating': perf.details['note'] if ('note' in perf.details
                                                         and perf.temps_de_jeu >= services.PLAYTIME['MAX_LONG'])
                      else None,
                      'joueur': perf.joueur}
        position = perf.joueur.poste
        if position is not None:
            if position == 'G':
                base_stats['against'] = perf.details['stats']['goals_conceded']
                base_stats['saves'] = perf.details['stats']['goals_saved']
            out[position].append(base_stats)
    # meilleur de chaque poste
    for pos in ['D', 'M']:
        best = 0
        for rt in (st['rating'] for st in out[pos]):
            if rt is not None:
                best = max(best, rt)
        for p in out[pos]:
            p['best'] = p['rating'] == best
    return out


@register.filter()
def format_scorer(joueur, stat):
    if stat[joueur] == 1:
        return joueur.__str__()
    else:
        return joueur.__str__() + ' x%d' % stat[joueur]


@register.inclusion_tag('game/tags/l1results_keyvalue.html')
def keyvalue(key, val, falogo=None, classname='kvgroup'):
    return {'key': key, 'value': val, 'falogo': falogo, 'classname': classname}
