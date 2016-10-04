__author__ = 'mgrandrie'
"""
Utilitaire de conversion et d'agglomération des notes "brutes" importées
"""


def compute_note(statnuts_ratings):
    notes = []
    for r in statnuts_ratings:
        notes.append(
            CONVERSION_FUNCTIONS[r['source']](float(r['rating'])) if r['source'] in CONVERSION_FUNCTIONS else float(
                r['rating']))
    return float(sum(notes)) / max(len(notes), 1)


def _conv_kicker(raw):
    return (1 - (float(raw) / 8)) * 10


def _conv_ws(raw):
    a = -0.5327483
    b = 2.409241
    c = 122.5656
    d = 254.007
    y = round(round((d + (a - d) / (1 + pow(10 * float(raw) / c, b))) / 5) / 2, 1)
    return y

CONVERSION_FUNCTIONS = {'04c19d53-ba15-11e4-97c6-b1229586dec7': _conv_ws,
                        '099e0a06-bba1-11e4-aabd-e33b7dc35c80': _conv_kicker}