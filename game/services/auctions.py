import random
from operator import attrgetter
from django.db import transaction
from django.utils import timezone

from game.models import transfer_models, league_models


class SaleSolvingException(Exception):
    pass


@transaction.atomic()
def solve_session(merkato_session):
    assert merkato_session.merkato.mode in ['BID', 'DRFT'], merkato_session.merkato.mode
    if merkato_session.closing > timezone.now():
        raise SaleSolvingException('Merkato session not over yet, closing time is %s' % merkato_session.closing)
    if merkato_session.merkato.mode == 'BID':
        # first, apply releases
        for release in transfer_models.Release.objects.filter(merkato_session=merkato_session):
            league_models.BankAccount.objects.release(release)
            release.signing.end = timezone.now()
            release.done = True
            release.signing.save()
            release.save()
        # budgets and rosters are done, now solve.
        sales = sorted(merkato_session.sale_set.all(), key=attrgetter('rank'))
        # resolution must be sequential:
        for s in sales:
            solve_sale(s)
    elif merkato_session.merkato.mode == 'DRFT':
        # TODO draft
        pass
    merkato_session.is_solved = True
    merkato_session.save()
    return merkato_session


@transaction.atomic()
def solve_sale(sale):
    auctions = sale.auctions.all()
    processed_auctions = [_validate_auction(auc) for auc in auctions]
    valid_auctions = [auc for auc in processed_auctions if auc.is_valid]
    if not valid_auctions:
        _handle_no_auction(sale)
    else:
        winner = _find_winner(valid_auctions)
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


@transaction.atomic()
def _validate_auction(auction):
    try:
        auction.validate()
        auction.is_valid = True
    except transfer_models.Auction.AuctionNotValidException as e:
        auction.is_valid = False
        auction.reject_cause = e.code
    auction.save()
    return auction


