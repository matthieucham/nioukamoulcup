import random
import json
from math import ceil
import decimal
from operator import attrgetter
from django.db import transaction
from django.db.models import FilteredRelation, Q
from django.utils import timezone

from utils import locked_atomic_transaction
from game.models import transfer_models, league_models
from ligue1.models import Joueur


class SaleSolvingException(Exception):
    pass


@transaction.atomic
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


@transaction.atomic
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
            league_models.Signing.objects.end(signing, 'MV', amount=sale.get_selling_price())
            league_models.BankAccount.objects.sell(sale)
            # start new contract:
            league_models.Signing.objects.create(player=sale.player, team=sale.winning_auction.team,
                                                 league_instance=sale.merkato_session.merkato.league_instance,
                                                 attributes=_make_signing_attr(sale))
            league_models.BankAccount.objects.buy(sale)
        else:
            pass  # nothing to do (no buyer)


def _make_signing_attr(sale):
    return {'amount': float(sale.get_buying_price().quantize(decimal.Decimal('.1'), rounding=decimal.ROUND_HALF_UP)),
            'type': sale.type,
            'release_amount': float((sale.get_buying_price() * decimal.Decimal(
                1.0 - sale.merkato_session.merkato.configuration.get('re_tax_rate'))).quantize(decimal.Decimal('.1'),
                                                                                               rounding=decimal.ROUND_HALF_UP)),
            'locked': False,
            'score_factor': sale.merkato_session.attributes.get('score_factor', 1.0)}


@transaction.atomic
def solve_session(merkato_session):
    assert merkato_session.merkato.mode == 'BID'
    if merkato_session.solving > timezone.now():
        raise SaleSolvingException('Merkato session not over yet, solving time is %s' % merkato_session.solving)
    # first, apply releases
    for release in transfer_models.Release.objects.filter(merkato_session=merkato_session):
        league_models.BankAccount.objects.release(release)
        league_models.Signing.objects.end(release.signing, 'RE', date=timezone.now(), amount=release.amount)
        release.done = True
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


@transaction.atomic
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


@transaction.atomic
def _validate_auction(auction):
    try:
        auction.validate()
        auction.is_valid = True
    except transfer_models.Auction.AuctionNotValidException as e:
        auction.is_valid = False
        auction.reject_cause = e.code
    auction.save()
    return auction


@transaction.atomic
def solve_draft_session(draft_session):
    assert draft_session.merkato.mode == 'DRFT'
    if draft_session.closing > timezone.now():
        raise SaleSolvingException('Draft session not over yet, solving time is %s' % draft_session.closing)
    app = list()
    for rk in draft_session.draftsessionrank_set.order_by('rank'):
        pl = solve_draft_pick(rk, app)
        if pl is not None:
            app.append(pl)
    draft_session.is_solved = True
    draft_session.save()


@transaction.atomic
def solve_draft_pick(draft_session_rank, already_picked_players):
    for pick in draft_session_rank.picks.order_by('pick_order').all():
        if pick.player not in already_picked_players:
            if available_for_pa(pick.player, draft_session_rank.team.division,
                                draft_session_rank.draft_session.merkato.league_instance):
                _do_draft_signing(pick)
                return pick.player
            else:
                print('Joueur %s plus dispo pour la draft' % pick.player.display_name())
    return None


@transaction.atomic
def _do_draft_signing(draft_pick):
    signing = league_models.Signing.objects.create(
        player=draft_pick.player,
        team=draft_pick.draft_session_rank.team,
        league_instance=draft_pick.draft_session_rank.draft_session.merkato.league_instance,
        attributes=_make_draft_signing_attr(draft_pick)
    )
    draft_pick.draft_session_rank.signing = signing
    draft_pick.draft_session_rank.save()


def _make_draft_signing_attr(draft_pick):
    return {'rank': draft_pick.draft_session_rank.rank,
            'pick_order': draft_pick.pick_order,
            'type': 'DRFT',
            'locked': True,
            'score_factor': draft_pick.draft_session_rank.draft_session.merkato.configuration.get('score_factor', 1.0)}


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
    if merkato.last_solving < timezone.now():
        return False, 'TOO_LATE'
    expired_sessions = merkato.merkatosession_set.filter(solving__lt=timezone.now()).count()
    current_pa = transfer_models.Sale.objects.filter(merkato_session__merkato=merkato,
                                                     merkato_session__solving__gt=timezone.now(),
                                                     type='PA',
                                                     team=team).count()
    previous_pas = transfer_models.Sale.objects.filter(merkato_session__merkato=merkato,
                                                       merkato_session__solving__lt=timezone.now(),
                                                       type='PA',
                                                       team=team).count()
    if merkato.configuration.get('pa_mandatory', False):
        return current_pa + previous_pas > 0, 'NOT_ENOUGH_PA'
    if current_pa > 0:
        return True, 'CURRENT_PA'
    if expired_sessions < 16:
        return True, 'BEGINNING'
    if expired_sessions // 8 <= previous_pas:
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
    if merkato.end < timezone.now():
        return False, 'TOO_LATE'
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
    if merkato.end < timezone.now():
        return False, 'TOO_LATE'
    current_mv_count = transfer_models.Sale.objects.filter(merkato_session__merkato=merkato,
                                                           merkato_session__solving__gt=timezone.now(),
                                                           type='MV',
                                                           team=team).count()
    if current_mv_count >= merkato.configuration.get('mv_number'):
        return False, 'CURRENT_MV'
    return True, None


def available_for_pa(joueur, division, instance):
    c1 = league_models.Signing.objects.filter(team__division=division,
                                              end__isnull=True,
                                              league_instance=instance,
                                              player=joueur).count()
    c2 = transfer_models.Sale.objects.filter(merkato_session__is_solved=False).filter(team__division=division,
                                                                                      merkato_session__merkato__league_instance=instance,
                                                                                      player=joueur).count()
    return c1 + c2 == 0


def available_for_mv(joueur, team, instance):
    return Joueur.objects.filter(signing__team=team, signing__begin__lt=timezone.now(), signing__end__isnull=True,
                                 signing__league_instance=instance).filter(pk=joueur.pk).count() == 1


@transaction.atomic
def solve_transition_session(transition_session):
    ntk = int(transition_session.attributes.get('to_keep'))
    li = transition_session.merkato.league_instance
    day = league_models.LeagueInstancePhaseDay.objects.get_latest_day_for_phases(
        league_models.LeagueInstancePhase.objects.filter(league_instance=li, type='FULLSEASON'))[0]
    latest_tds = league_models.TeamDayScore.objects.filter(day=day)
    for team in league_models.Team.objects.filter(league=li.league):
        choice = team.transitionteamchoice_set.filter(transition_session=transition_session).first()
        if choice is None:
            team.attributes['formation'] = dict(transition_session.attributes.get('default_formation'))
        else:
            team.attributes['formation'] = dict(choice.formation_to_choose)
            for sg in choice.signings_to_free.all():
                league_models.SigningManager.objects.end(sg, 'FR')
        _fix_signings(team, ntk, latest_tds.get(team=team), li)


def _fix_signings(team, nb_to_keep, team_tds, instance):
    if nb_to_keep < team.signing_set.filter(league_instance=instance, end__isnull=True).count():
        nb_to_free = team.signing_set.filter(league_instance=instance, end__isnull=True).count() - nb_to_keep
        # il faut virer les joueurs qui ont le score le plus faible parmi ceux qui restent
        pl_list = []
        if team_tds is not None:
            compo = team_tds.attributes.get('composition')
            for _, pls in compo.items():
                for pl in pls:
                    pl_list.append((pl['player']['id'], pl['score']))
        sorted(pl_list, key=lambda tup: float(tup[1])).reverse()
        # virer d'abord ceux qui ne sont même pas dans la liste
        in_list = [plid for plid, score in pl_list]
        signings_not_in_list = league_models.Signing.objects.filter(team=team, league_instance=instance,
                                                                    end__isnull=True).exclude(
            player__id__in=in_list).all()
        to_free = signings_not_in_list[:nb_to_free]
        for sg in to_free:
            league_models.Signing.objects.end(sg, 'FR')
        nb_to_free -= len(to_free)
        if nb_to_free > 0:
            # il en reste !
            # ici les premiers éléments de la liste sont ceux à virer
            to_free = [plid for plid, score in pl_list[:nb_to_free]]
            for sg in league_models.Signing.objects.filter(team=team, league_instance=instance,
                                                           end__isnull=True).filter(player__id__in=to_free):
                league_models.Signing.objects.end(sg, 'FR')
    # Verrouiller les signatures qu'il reste
    for sg in league_models.Signing.objects.filter(team=team, league_instance=instance, end__isnull=True):
        sg.attributes['locked'] = True
        sg.save()
