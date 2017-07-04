from django.test import TestCase

from game import models
from game.services import auctions
from ligue1 import models as l1models


class TransferTestCase(TestCase):
    def setUp(self):
        self.targeted_player = l1models.Joueur(nom='Bamougui', poste='A', sn_person_uuid='uuid')
        self.league = models.League(name='Test League', mode='KCUP')
        self.instance = models.LeagueInstance(name='Test Instance', )
        self.division = models.LeagueDivision(league=self.league, level=1, name='Test division 1', capacity=20)
        self.merkato_bid = models.Merkato(mode='BID', league_instance=self.instance)
        self.merkato_bid_session = models.MerkatoSession(merkato=self.merkato_bid, number=1)

        self.author_team = models.Team(name='PAMAKER', league=self.league, division=self.division)
        self.sale_to_solve = models.Sale(player=self.targeted_player, team=self.author_team,
                                         merkato_session=self.merkato_bid_session)

    def test_pa_nominal_3_auctions(self):
        self.sale_to_solve.type = 'PA'
        self.sale_to_solve.min_price = 0.1

        bidder_1 = models.Team(name='BIDDER1', league=self.league, division=self.division)
        bidder_2 = models.Team(name='BIDDER2', league=self.league, division=self.division)
        auction_1 = models.Auction(sale=self.sale_to_solve, team=bidder_1, value='5.1')
        auction_2 = models.Auction(sale=self.sale_to_solve, team=bidder_2, value='4.2')
        auction_3 = models.Auction(sale=self.sale_to_solve, team=self.author_team, value='3.4')
        self.sale_to_solve.auctions.add(auction_1, auction_2, auction_3)

        auctions.solve_sale(self.sale_to_solve)

        self.assertTrue(auction_1.is_valid)
        self.assertTrue(auction_2.is_valid)
        self.assertTrue(auction_3.is_valid)
        self.assertEqual(self.sale_to_solve.winning_auction, auction_1)
