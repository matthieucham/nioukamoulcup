import random
from operator import attrgetter
from django.db import transaction
from django.utils import timezone


class SaleSolvingException(Exception):
    pass


@transaction.atomic()
def solve_session(merkato_session):
    if merkato_session.closing > timezone.now():
        raise SaleSolvingException('Merkato session not over yet, closing time is %s' % merkato_session.closing)
    sales = sorted(merkato_session.sale_set.all(), key=attrgetter('rank'))
    # resolution must be sequential:
    for s in sales:
        solve_sale(s)
    merkato_session.is_solved = True
    merkato_session.save()
    return merkato_session


@transaction.atomic()
def solve_sale(sale):
    auctions = sale.auctions.all()
    processed_auctions = [_validate_auction(auc) for auc in auctions]  # list of (auction, is_valid)
    if not processed_auctions:
        _handle_no_auction(sale)
    else:
        winner = _find_winner(processed_auctions)
        _set_winning_auction(winner)
    return sale


def _set_winning_auction(auction):
    auction.sale.winning_auction = auction
    auction.sale.save()


def _find_winner(processed_auctions):
    # sort by highest vaalue
    sorted_auctions = sorted(processed_auctions, key=lambda a: a.value, reverse=True)
    max_val = sorted_auctions[0].value
    possible_winners = [auc for auc in sorted_auctions if auc.value == max_val]
    # pick one in possible_winners
    if len(possible_winners) == 1:
        return possible_winners[0]
    else:
        secure_random = random.SystemRandom()
        winner = secure_random.choice(possible_winners)
        return winner


def _handle_no_auction(sale):
    sale.winning_auction = None
    sale.save()


def _validate_auction(auction):
    auction.is_valid = True  # TODO
    auction.save()
    return auction


