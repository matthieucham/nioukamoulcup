from utils.timer import Timer

BONUS = {
    'COLLECTIVE': {
        'CLEANSHEET': {'G': 3.4, 'D': 2.5, 'M': 1.0, 'A': 0},
        'HALFCLEANSHEET': {'G': 1.7, 'D': 1.25, 'M': 0.5, 'A': 0},
        'OFFENSIVE': {'G': 0, 'D': 0, 'M': 0.4, 'A': 1},
        'HALFOFFENSIVE': {'G': 0, 'D': 0, 'M': 0.2, 'A': 0.5}
    },
    'PERSONAL': {
        'LEADER': {'G': 0, 'D': 1.2, 'M': 0.6, 'A': 0},
        '3STOPS': {'G': 0.9, 'D': 0, 'M': 0, 'A': 0},
        'PENALSTOP': {'G': 3, 'D': 3, 'M': 3, 'A': 3},
        'GOAL': {'G': 3, 'D': 3, 'M': 3, 'A': 3},
        'PENALTY': {'G': 1.5, 'D': 1.5, 'M': 1.5, 'A': 1.5},
        'PASS': {'G': 2, 'D': 2, 'M': 2, 'A': 2},
        'HALFPASS': {'G': 1, 'D': 1, 'M': 1, 'A': 1}
    }
}

PLAYTIME = {'MAX_SHORT': 15, 'MAX_LONG': 30, 'MIN_BONUS': 45}

COMPENSATION = {'SHORT': 1, 'LONG': 2, 'CANCELLED': 5}

SALARY_SCORE_BOUNDS = [(6.1, 'cl1'), (6.3, 'cl2'), (6.3, 'cl3'), (6.5, 'cl4'), (6.75, 'cl5'), (7.1, 'cl6'),
                       (7.6, 'cl7'),
                       (8, 'cl8'), (8.4, 'cl9'), (8.9, 'cl10')]


def compute_best_by_position(all_perfs):
    with Timer(id='compute_best_by_position', verbose=False):
        best_by_position = {'dom': {'G': 0, 'D': 0, 'M': 0, 'A': 0}, 'ext': {'G': 0, 'D': 0, 'M': 0, 'A': 0}}
        for pj in all_perfs:
            if pj.joueur.poste is None:
                continue
            if 'note' in pj.details and pj.temps_de_jeu >= PLAYTIME['MAX_LONG'] and pj.details['note'] is not None:
                best_by_position[pj.details['equipe']][pj.joueur.poste] = max(pj.details['note'],
                                                                              best_by_position[pj.details['equipe']][
                                                                                  pj.joueur.poste])
        return best_by_position


def compute_score_performance(perf, best_note_by_position):
    with Timer(id='compute_score_performance', verbose=False):
        if perf.joueur.poste is None:
            return None, 0, None
        if perf.temps_de_jeu < PLAYTIME['MAX_SHORT']:
            return None, _compute_bonus(perf, False, best_note_by_position), COMPENSATION['SHORT']
        elif perf.temps_de_jeu < PLAYTIME['MAX_LONG']:
            return None, _compute_bonus(perf, False, best_note_by_position), COMPENSATION['LONG']
        elif perf.temps_de_jeu < PLAYTIME['MIN_BONUS']:
            return perf.details['note'] if 'note' in perf.details else None, _compute_bonus(perf, False,
                                                                                            best_note_by_position), None if 'note' in perf.details else \
                       COMPENSATION['LONG']
        else:
            return perf.details['note'] if 'note' in perf.details else None, _compute_bonus(perf, True,
                                                                                            best_note_by_position), None if 'note' in perf.details else \
                       COMPENSATION['LONG']


def _compute_bonus(perf, has_collective_bonus, best_note_by_position):
    poste = perf.joueur.poste
    base = 0
    # bonus individuel
    for (i, j) in [('PENALSTOP', 'penalties_saved'), ('GOAL', 'goals_scored'), ('PENALTY',
                                                                              'penalties_scored'),
                   ('PASS', 'goals_assists'), ('HALFPASS', 'penalties_awarded')]:
        base += (BONUS['PERSONAL'][i][poste] * perf.details['stats'][j])
    if perf.details['stats']['goals_saved'] > 3:
        base += BONUS['PERSONAL']['3STOPS'][poste]
    if 'note' in perf.details and perf.details['note'] >= best_note_by_position[perf.details['equipe']][poste]:
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