import random


class SaleSolvingException(Exception):
    pass


def solve_sale(sale):
    auctions = sale.auctions.all()
    processed_auctions = [(auc, _validate_auction(auc)) for auc in auctions]  # list of (auction, is_valid)
    if not processed_auctions:
        _handle_no_auction(sale)
    else:
        winner = _find_winner(processed_auctions)
        _set_winning_auction(winner)


def _set_winning_auction(auction):
    auction.sale.winning_auction = auction


def _find_winner(processed_auctions):
    # sort by highest vaalue
    sorted(processed_auctions, key=lambda a: a[0].value, reverse=True)
    max_val = processed_auctions[0][0].value
    possible_winners = [auc for auc in processed_auctions if auc[0].value == max_val]
    # pick one in possible_winners
    if len(possible_winners) == 1:
        return possible_winners[0]
    else:
        secure_random = random.SystemRandom()
        winner = secure_random.choice(possible_winners)
        return winner


def _handle_no_auction(sale):
    sale.winning_auction = None


def _validate_auction(auction):
    auction.is_valid = True  # TODO
    return auction.is_valid


