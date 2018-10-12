__author__ = 'mgrandrie'
import operator
from django import template
from django.template import defaultfilters

from ligue1 import models as l1models
from game import services
from game.models import JJScore

register = template.Library()


@register.inclusion_tag('game/tags/l1results_rencontre_score.html')
def rencontre_score(rencontre, with_logos=False):
    if rencontre.resultat is None:
        score_dom = '?'
        score_ext = '?'
    else:
        score_dom = rencontre.resultat['dom']['buts_pour']
        score_ext = rencontre.resultat['ext']['buts_pour']
    if hasattr(rencontre, 'diff'):
        diff = rencontre.diff
    else:
        diff = 0
    return {
        'rid': rencontre.pk,
        'cdom': rencontre.club_domicile,
        'cext': rencontre.club_exterieur,
        'score_dom': score_dom,
        'score_ext': score_ext,
        'diff': diff,
        'logos': with_logos
    }


@register.inclusion_tag('game/tags/l1results_last_journees.html')
def last_journees(nb=1):
    """
    Retourne les résultats de la dernière journée enregistrée
    :param nb:
    :return:
    """
    journees = l1models.Journee.objects.filter(saison__est_courante__isnull=False).order_by('-fin')[:nb]
    return {'journees': sorted(journees, key=operator.attrgetter('fin'))}


def sort_position_function(joueur):
    sort_order = {'G': 0, 'D': 1, 'M': 2, 'A': 3, None: 10}
    return sort_order[joueur.poste]


@register.inclusion_tag('game/tags/l1results_club_logo.html')
def club_logo(club, size='medium'):
    mapping = {'small': 32, 'medium': 48, 'big': 64, 'biggest': 128}
    return {'svg': club.maillot_svg if club else 'jersey-noclub2',
            'stroke': club.maillot_color_stroke if club else '#FFFFFF', 'fill': club.maillot_color_bg if club else '',
            'size': mapping.get(size, mapping.get('medium'))}


@register.inclusion_tag('game/tags/l1results_team_players.html')
def joueurs_club(club):
    """
    Retourne la liste des joueurs de ce club
    :param club:
    :return:
    """
    if club is not None:
        joueurs = l1models.Joueur.objects.filter(club=club).order_by('nom')
    else:
        joueurs = l1models.Joueur.objects.filter(
            performances__rencontre__journee__saison__est_courante__isnull=False).distinct().order_by('nom')
    return {'team': 'Hors L1' if club is None else club, 'players': sorted(joueurs, key=sort_position_function)}


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
        for key in ['goals_scored', 'goals_assists', 'penalties_scored', 'penalties_awarded', 'penalties_saved',
                    'own_goals']:
            if perf.details['stats'][key] > 0:
                if key not in agglo:
                    agglo[key] = {'dom': {}, 'ext': {}}
                agglo[key][perf.details['equipe']][perf.joueur] = perf.details['stats'][key]
    return \
        {
            'summary': agglo,
            'header': {
                'date': rencontre.date,
                'dom': rencontre.club_domicile,
                'ext': rencontre.club_exterieur,
                'score_dom': rencontre.resultat['dom']['buts_pour'],
                'score_ext': rencontre.resultat['ext']['buts_pour']}
        }


@register.inclusion_tag('game/tags/l1results_rencontre_team.html')
def rencontre_team(rencontre, equipe):
    out = {'G': [], 'D': [], 'M': [], 'A': []}
    jjs_dict = dict(JJScore.objects.filter(rencontre=rencontre).values_list('joueur', 'details'))
    for perf in rencontre.performances.filter(details__equipe=equipe):
        base_stats = {'time': perf.temps_de_jeu,
                      'rating': perf.details['note'] if ('note' in perf.details
                                                         and perf.temps_de_jeu >= services.PLAYTIME['MAX_LONG'])
                      else None,
                      'joueur': perf.joueur,
                      'bonuses': jjs_dict.get(perf.joueur.pk).get('bonuses') or None}
        position = perf.joueur.poste
        out[position].append(base_stats)
    return out


@register.filter()
def format_scorer(joueur, stat):
    if stat[joueur] == 1:
        return joueur.display_name()
    else:
        return joueur.display_name() + ' x%d' % stat[joueur]


@register.inclusion_tag('game/tags/l1results_keyvalue.html')
def keyvalue(key, val, classname='kvgroup'):
    return {'key': key, 'value': val if val is not None else '-', 'classname': classname}


@register.inclusion_tag('game/tags/l1results_bonusvalue.html')
def bonusvalue(bonuskey, poste, label, val):
    if (services.BONUS['COLLECTIVE'].get(bonuskey) or services.BONUS['PERSONAL'].get(bonuskey))[poste] > 0:
        return {'bonuskey': bonuskey, 'poste': poste, 'label': label, 'value': val if val is not None else '-',
                'masked': False}
    else:
        return {'masked': True}


@register.inclusion_tag('game/tags/l1results_performance_joueur.html')
def perf_joueur(jjs):
    # TODO order
    # TODO bonus agg
    return {'jjs': jjs}


@register.inclusion_tag('game/tags/l1results_bonus.html')
def bonus(bonuskey, position, bonusval=1):
    icon_dict = {
        'GOAL': ('fa-trophy', 'Tomato'),
        'PENALTY': ('fa-trophy fa-rotate-90', 'Orange'),
        'PASS': ('fa-gift', 'DodgerBlue'),
        'HALFPASS': ('fa-ambulance', 'Sienna'),
        'LEADER': ('fa-plus-circle', 'MediumSeaGreen'),
        'PENALSTOP': ('fa-ban', 'SlateBlue'),
        'CLEANSHEET': ('fa-shield', 'Gray'),
        'HALFCLEANSHEET': ('fa-shield fa-rotate-90', 'LightGray'),
        'OFFENSIVE': ('fa-thermometer-full', 'GoldenRod'),
        'HALFOFFENSIVE': ('fa-thermometer-half', 'Gold'),
        'CSC': ('fa-thumbs-down', 'DarkSlateGrey'),
    }
    if bonuskey == 'CSC' or (services.BONUS['COLLECTIVE'].get(bonuskey) or services.BONUS['PERSONAL'].get(bonuskey))[
        position] > 0:
        ico, color = icon_dict[bonuskey]
        return {'icon': ico, 'color': color, 'nb': bonusval, 'masked': False}
    else:
        return {'masked': True}


@register.inclusion_tag('game/tags/l1results_compo_player.html')
def compo_player(jjs):
    # TODO if no club
    if hasattr(jjs, 'note'):
        if jjs.note is not None:
            note = '%0.1f' % jjs.note
        else:
            note = '-'
    else:
        note = '%0.1f [%dn]' % (jjs.avg_note, jjs.nb_notes)
    if hasattr(jjs, 'total_bonuses'):
        tb = '%0.1f' % jjs.total_bonuses
    else:
        tb = None
    return {
        'club': jjs.joueur.club,
        'joueur': jjs.joueur,
        'note': note,
        'total_bonuses': tb,
        'bonus': jjs.details['bonuses'] if 'bonuses' in jjs.details else None
    }
