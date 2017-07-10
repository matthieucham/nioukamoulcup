import random
import json
from operator import attrgetter
from django.db import transaction
from django.utils import timezone

from utils import locked_atomic_transaction
from game.models import transfer_models, league_models


class SaleSolvingException(Exception):
    pass


@transaction.atomic()
def apply_transfers(merkato_session):
    assert merkato_session.is_solved
    for sale in merkato_session.sale_set.all():
        _do_transfer(sale)


@transaction.atomic()
def _do_transfer(sale):
    if sale.type == 'PA':
        if sale.winning_auction is None:
            # transfer to author
            league_models.Signing.objects.create(player=sale.player, team=sale.team,
                                                 attributes=_make_signing_attr(sale))
        else:
            league_models.Signing.objects.create(player=sale.player, team=sale.winning_auction,
                                                 attributes=_make_signing_attr(sale))
        league_models.BankAccount.objects.buy(sale)
    elif sale.type == 'MV':
        if sale.winning_auction is not None:
            # end contract with selling team:
            league_models.Signing.objects.filter(player=sale.player, team=sale.team, end__isnull=True).update(
                end=timezone.now())
            league_models.BankAccount.objects.sell(sale)
            # start new contract:
            league_models.Signing.objects.create(player=sale.player, team=sale.winning_auction,
                                                 attributes=_make_signing_attr(sale))
            league_models.BankAccount.objects.buy(sale)
        else:
            pass  # nothing to do (no buyer)


def _make_signing_attr(sale):
    return json.dumps({'amount': sale.get_buying_price()})  # TODO


@transaction.atomic()
def solve_session(merkato_session):
    assert merkato_session.merkato.mode == 'BID'
    if merkato_session.closing > timezone.now():
        raise SaleSolvingException('Merkato session not over yet, closing time is %s' % merkato_session.closing)
    # first, apply releases
    for release in transfer_models.Release.objects.filter(merkato_session=merkato_session):
        league_models.BankAccount.objects.release(release)
        release.signing.end = timezone.now()
        release.done = True
        release.signing.save()
        release.save()
    with locked_atomic_transaction.LockedAtomicTransaction(
            league_models.BankAccount):  # prevents changes in BankAccount balance during resolution
        # budgets and rosters are done, now solve.
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


