import random


class SaleSolvingException(Exception):
    pass


def solve_sale(sale):
    auctions = sale.auctions.all()
    if not auctions:
        handle_no_auction(sale, noauction=True)
    else:
        for auc in auctions:
            valid_auctions = []
            invalid_auctions = dict()
            try:
                validate_auction(auc)
                valid_auctions.append(auc)
            except SaleSolvingException as e:
                invalid_auctions[auc] = e.message
        if not valid_auctions:
            handle_no_auction(sale, noauction=False)
        else:
            sorted(valid_auctions, key=lambda a: a.value, True)
            possible_winners = []
            max_val = 0
            for auc in valid_auctions:
                if auc.value >= max_val:
                    possible_winners.append(auc)
                else:
                    break
            # pick one in possible_winners
            if len(possible_winners) == 1:
                winner = possible_winners[0]
            else:
                secure_random = random.SystemRandom()
                winner = secure_random.choice(possible_winners)
            return winner, valid_auctions, invalid_auctions


def handle_no_auction(sale, noauction=False):
    if sale.type == 'MV':
        cancel_mv(sale, no_auction=noauction)
    else:
        raise SaleSolvingException('a PA or AM requires at least one auction : the one of the initial auctioner')


def validate_auction(auction):
    pass  # TODO


def cancel_mv(sale, no_auction=False, no_valid_auction=True):
    pass  # TODO
