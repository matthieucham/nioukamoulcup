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
        _unblock_min_price(sale)


def _unblock_min_price(sale):
    if sale.type == 'PA':
        account = league_models.BankAccount.objects.get(team=sale.team)
        account.blocked -= sale.min_price
        account.save()


@transaction.atomic()
def _do_transfer(sale):
    if sale.type == 'PA':
        winner, value = sale.get_winner_and_price()  # winner cannot be None (PA)
        league_models.Signing.objects.create(player=sale.player, team=winner,
                                             league_instance=sale.merkato_session.merkato.league_instance,
                                             attributes=_make_signing_attr(sale))
        league_models.BankAccount.objects.buy(sale)
    elif sale.type == 'MV':
        if sale.winning_auction is not None:
            # end contract with selling team:
            signing = league_models.Signing.objects.get(player=sale.player, team=sale.team, end__isnull=True,
                                                        league_instance=sale.merkato_session.merkato.league_instance)
            league_models.Signing.objects.end(signing, 'MV', sale.get_selling_price())
            league_models.BankAccount.objects.sell(sale)
            # start new contract:
            league_models.Signing.objects.create(player=sale.player, team=sale.winning_auction,
                                                 league_instance=sale.merkato_session.merkato.league_instance,
                                                 attributes=_make_signing_attr(sale))
            league_models.BankAccount.objects.buy(sale)
        else:
            pass  # nothing to do (no buyer)


def _make_signing_attr(sale):
    return json.dumps({'amount': float(sale.get_buying_price()), 'type': sale.type,
                       'score_factor': sale.merkato_session.merkato.configuration[
                           'score_factor'] if 'score_factor' in sale.merkato_session.merkato.configuration else 1.0})


@transaction.atomic()
def solve_session(merkato_session):
    assert merkato_session.merkato.mode == 'BID'
    if merkato_session.solving > timezone.now():
        raise SaleSolvingException('Merkato session not over yet, solving time is %s' % merkato_session.solving)
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


def can_register_auction(team, merkato):
    """
    Vérifie que cette ékyp est autorisée à envoyer des enchères. La règle:
    - avoir une PA en cours
    ou bien
    - en être dans les 3 premières sessions d'un merkato
    ou bien
    - avoir déjà posté (N/2 -1) PA où N est le nombre de sessions écoulées
    :return: True |False
    """
    expired_sessions = merkato.merkatosession_set.filter(solving__lt=timezone.now()).count()
    if expired_sessions < 4:
        return True, 'BEGINNING'
    current_pa = transfer_models.Sale.objects.filter(merkato_session__merkato=merkato,
                                                     merkato_session__solving__gt=timezone.now(),
                                                     type='PA',
                                                     team=team).count()
    if current_pa > 0:
        return True, 'CURRENT_PA'
    previous_pas = transfer_models.Sale.objects.filter(merkato_session__merkato=merkato,
                                                       merkato_session__solving__lt=timezone.now(),
                                                       type='PA',
                                                       team=team).count()
    if (expired_sessions // 2) - 1 <= previous_pas:
        return True, 'ENOUGH_PA'
    else:
        return False, 'NOT_ENOUGH_PA'


def can_register_pa(team, merkato):
    """
    Vérifie que cette ékyp est autorisée à envoyer une PA. La règle:
    - pas de PA en cours
    - avoir une place dans la team (TODO)
    :return: True |False
    """
    current_pa_count = transfer_models.Sale.objects.filter(merkato_session__merkato=merkato,
                                                           merkato_session__solving__gt=timezone.now(),
                                                           type='PA',
                                                           team=team).count()
    current_roster = team.signing_set.filter(league_instance=merkato.league_instance, end__isnull=True).count()
    if current_pa_count >= merkato.configuration.get('pa_number'):
        return False, 'CURRENT_PA'
    if current_roster >= merkato.configuration.get('roster_size_max'):
        return False, 'ROSTER_FULL'
    return True, None


def can_register_mv(team, merkato):
    """
    Vérifie que cette ékyp est autorisée à envoyer une MV. La règle:
    - pas de MV en cours
    :return: True |False
    """
    current_mv_count = transfer_models.Sale.objects.filter(merkato_session__merkato=merkato,
                                                           merkato_session__solving__gt=timezone.now(),
                                                           type='MV',
                                                           team=team).count()
    if current_mv_count >= merkato.configuration.get('mv_number'):
        return False, 'CURRENT_MV'
    return True, None
