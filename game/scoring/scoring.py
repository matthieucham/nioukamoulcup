__author__ = 'mgrandrie'
from ligue1 import models as l1models
from game import models


BONUS = {
    'COLLECTIVE': {
        'CLEANSHEET': {'G': 3.4, 'D': 2.5, 'M': 1.0, 'A': 0},
        'HALFCLEANSHEET': {'G': 1.7, 'D': 1.25, 'M': 0.5, 'A': 0},
        'OFFENSIVE': {'G': 0, 'D': 0, 'M': 0.4, 'A': 1},
        'HALFOFFENSIVE': {'G': 0, 'D': 0, 'M': 0.2, 'A': 0.5}
    },
    'PERSONAL': {
        'LEADER': {'G': 0, 'D': 1.2, 'M': 0.6, 'A': 0},
        'CONCEDED': {'G': -1.2, 'D': 0, 'M': 0, 'A': 0},
        'SAVE': {'G': 0.4, 'D': 0, 'M': 0, 'A': 0},
        'GOAL': {'G': 3, 'D': 3, 'M': 3, 'A': 3},
        'PENALTY': {'G': 1.5, 'D': 1.5, 'M': 1.5, 'A': 1.5},
        'PASS': {'G': 2, 'D': 2, 'M': 2, 'A': 2},
        'HALFPASS': {'G': 1, 'D': 1, 'M': 1, 'A': 1}
    }
}

PLAYTIME = {'MAX_SHORT': 15, 'MAX_LONG': 30, 'MIN_BONUS': 45}

COMPENSATION = {'SHORT': 1, 'LONG': 3, 'CANCELLED': 5}


def _compute_score(perf, best_note_by_position):
    if perf.temps_de_jeu < PLAYTIME['MAX_SHORT']:
        None, _compute_bonus(perf, False, best_note_by_position), COMPENSATION['SHORT']
    elif perf.temps_de_jeu < PLAYTIME['MAX_LONG']:
        None, _compute_bonus(perf, False, best_note_by_position), COMPENSATION['LONG']
    elif perf.temps_de_jeu < PLAYTIME['MIN_BONUS']:
        perf.details['note'], _compute_bonus(perf, False, best_note_by_position), None
    else:
        perf.details['note'], _compute_bonus(perf, True, best_note_by_position), None


def _compute_bonus(perf, has_collective_bonus, best_note_by_position):
    poste = perf.joueur.poste
    base = 0
    # bonus individuel
    for (i, j) in [('CONCEDED', 'goals_conceded'), ('SAVE', 'goals_saved'), ('GOAL', 'goals_scored'), ('PENALTY',
                                                                                                       'penalties_scored'),
                   ('PASS', 'goals_assists'), ('HALFPASS', 'penalties_awarded')]:
        base += (BONUS['PERSONAL'][i][poste] * perf.details['stats'][j])
    if perf.details['note'] >= best_note_by_position[poste]:
        base += BONUS['PERSONAL']['LEADER'][poste]
    if has_collective_bonus:
        # get from rencontre...
        if perf.rencontre.resultat[perf.details['equipe']]['buts_contre'] == 0:
            base += BONUS['COLLECTIVE']['CLEANSHEET'][poste]
        if perf.rencontre.resultat[perf.details['equipe']]['buts_contre'] == 1 and perf.rencontre.resultat[
            perf.details['equipe']]['penos_contre'] == 1:
            base += BONUS['COLLECTIVE']['HALFCLEANSHEET'][poste]
        if perf.rencontre.resultat[perf.details['equipe']]['buts_pour'] == 3 and perf.rencontre.resultat[
            perf.details['equipe']]['penos_pour'] == 1:
            base += BONUS['COLLECTIVE']['HALFOFFENSIVE'][poste]
        if perf.rencontre.resultat[perf.details['equipe']]['buts_pour'] == 3 and perf.rencontre.resultat[
            perf.details['equipe']]['penos_pour'] == 0:
            base += BONUS['COLLECTIVE']['OFFENSIVE'][poste]
        if perf.rencontre.resultat[perf.details['equipe']]['buts_pour'] > 3:
            base += BONUS['COLLECTIVE']['OFFENSIVE'][poste]

    return base