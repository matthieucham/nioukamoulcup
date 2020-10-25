__author__ = 'mgrandrie'

from statistics import mean, stdev, median_low, StatisticsError

"""
Utilitaire de conversion et d'agglomération des notes "brutes" importées
"""


def _extract_sources(statnuts_roster):
    existing_sources = set()
    for ros in statnuts_roster:
        curr_srcs = set([r['source'] for r in ros['ratings']])
        existing_sources |= curr_srcs
    return existing_sources


def harmonize_notes(statnuts_roster):
    # calcul de la fonction de conversion par source
    by_src = dict()
    for src in _extract_sources(statnuts_roster):
        notes = [
            (CONVERSION_FUNCTIONS.get(r['source'],lambda n: n))(float(r['rating'])) for ros in statnuts_roster for
            r in ros['ratings'] if r['source'] == src
        ]
        if len(notes) > 1:
            by_src[src] = {'MEAN': mean(notes), 'STDEV': stdev(notes)}

    # application de la conversion sur chaque joueur
    def conv_func(n, m, s):
        if n is None:
            return None
        target_std = median_low([bs['STDEV'] for s, bs in by_src.items()])
        target_avg = median_low([bs['MEAN'] for s, bs in by_src.items()])
        if s == 0:
            return target_avg
        else:
            return (target_std / s) * (n - m) + target_avg

    for pl in statnuts_roster:
        try:
            pl['temp_note'] = mean(
                [conv_func((CONVERSION_FUNCTIONS.get(r['source'],lambda n: n))(float(r['rating'])), by_src[r['source']]['MEAN'], by_src[r['source']]['STDEV']) for r in
                 pl['ratings'] if r['source'] in by_src])
        except StatisticsError:
            pl['temp_note'] = None

    # calcul du nouveau facteur pour les temp_notes
    temp_notes = [pl['temp_note'] for pl in statnuts_roster if 'temp_note' in pl and pl['temp_note'] is not None]
    if len(temp_notes) == 0:
        # pas de notes !
        for pl in statnuts_roster:
            pl['hnote'] = None
        return statnuts_roster
    # for_hnotes = {'MEAN': mean(temp_notes), 'STDEV': stdev(temp_notes)}
    # calcul de la note finale:
    for pl in statnuts_roster:
        # converted = conv_func(pl.pop('temp_note'), for_hnotes['MEAN'], for_hnotes['STDEV'])
        converted = pl.get('temp_note', None)
        if converted is not None:
            pl['hnote'] = round(converted, 1)
        else:
            pl['hnote'] = None

    return statnuts_roster


def compute_note(statnuts_ratings):
    notes = []
    for r in statnuts_ratings:
        notes.append(
            (CONVERSION_FUNCTIONS.get(r['source']) or (lambda n: n))(float(r['rating'])))
    return round(float(sum(notes)) / max(len(notes), 1), 2)


def _conv_kicker(raw):
    return (1 - (float(raw) / 8)) * 10


def _conv_ws(raw):
    a = -0.5327483
    b = 2.409241
    c = 122.5656
    d = 254.007
    y = round(round((d + (a - d) / (1 + pow(10 * float(raw) / c, b))) / 5) / 2, 1)
    return y

def _conv_ws_new(raw):
    if raw < 3:
        return 1.1
    if raw < 4:
        return 1.6
    if raw < 4.3:
        return 2.1
    if raw < 4.8:
        return 2.6
    if raw < 5.2:
        return 3.1
    if raw < 5.6:
        return 3.6
    if raw < 6:
        return 4.1
    if raw < 6.4:
        return 4.6
    if raw < 6.7:
        return 5.1
    if raw < 7.1:
        return 5.6
    if raw < 7.4:
        return 6.1
    if raw < 7.8:
        return 6.6
    if raw < 8.1:
        return 7.1
    if raw < 8.4:
        return 7.6
    if raw < 8.8:
        return 8.1
    if raw < 9.1:
        return 8.6
    if raw < 9.5:
        return 9.1
    if raw < 9.9:
        return 9.6
    return 10.0

CONVERSION_FUNCTIONS = {'KICK': _conv_kicker, 'WHOSC': _conv_ws_new}
