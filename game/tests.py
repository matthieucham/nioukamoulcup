import uuid
from django.test import TestCase
from django.db import utils as dbutils

from game import models
from game.services import auctions
from ligue1 import models as l1models


class TransferTestCase(TestCase):
    def setUp(self):
        self.saison = l1models.Saison.objects.create(nom='Saison', sn_instance_uuid=uuid.uuid4(),
                                                     debut='2017-07-31',
                                                     fin='2018-06-01')
        self.targeted_player = l1models.Joueur.objects.create(nom='Bamougui', poste='A',
                                                              sn_person_uuid=uuid.uuid4())

        self.league = models.League.objects.create(name='Test League', mode='KCUP')
        self.instance = models.LeagueInstance.objects.create(name='Test Instance', begin='2017-09-01 09:00',
                                                             end='2017-10-15 21:00', configuration='{}',
                                                             league=self.league, saison=self.saison)
        self.division = models.LeagueDivision.objects.create(league=self.league, level=1, name='Test division 1',
                                                             capacity=20)
        self.merkato_bid = models.Merkato.objects.create(mode='BID', league_instance=self.instance,
                                                         begin='2017-09-01 09:00',
                                                         end='2017-10-15 21:00', configuration='{}')
        self.merkato_bid_session = models.MerkatoSession.objects.create(merkato=self.merkato_bid, number=1,
                                                                        closing='2017-10-01 21:00:00')

    def test_pa_nominal_3_auctions(self):
        author_team = models.Team.objects.create(name='PAMAKER', league=self.league, division=self.division,
                                                 attributes='')
        sale_to_solve = models.Sale.objects.create(player=self.targeted_player, team=author_team,
                                                   merkato_session=self.merkato_bid_session, type='PA',
                                                   min_price=0.1)

        bidder_1 = models.Team.objects.create(name='BIDDER1', league=self.league, division=self.division,
                                              attributes='')
        bidder_2 = models.Team.objects.create(name='BIDDER2', league=self.league, division=self.division,
                                              attributes='')
        auction_1 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_1, value='5.1')
        auction_2 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_2, value='4.2')
        auction_3 = models.Auction.objects.create(sale=sale_to_solve, team=author_team, value='3.4')
        sale_to_solve.auctions.add(auction_1, auction_2, auction_3)

        solved = auctions.solve_sale(sale_to_solve)

        self.assertTrue(models.Auction.objects.get(pk=auction_1.pk).is_valid)
        self.assertTrue(models.Auction.objects.get(pk=auction_2.pk).is_valid)
        self.assertTrue(models.Auction.objects.get(pk=auction_3.pk).is_valid)
        self.assertEquals(solved.winning_auction.pk, auction_1.pk)

    def test_pa_nominal_no_auction(self):
        author_team = models.Team.objects.create(name='PAMAKER', league=self.league, division=self.division,
                                                 attributes='')
        sale_to_solve = models.Sale.objects.create(player=self.targeted_player, team=author_team,
                                                   merkato_session=self.merkato_bid_session, type='PA',
                                                   min_price=0.1)
        solved = auctions.solve_sale(sale_to_solve)

        self.assertIsNone(solved.winning_auction)

    def test_pa_nominal_3_auctions_with_equality(self):
        author_team = models.Team.objects.create(name='PAMAKER', league=self.league, division=self.division,
                                                 attributes='')
        sale_to_solve = models.Sale.objects.create(player=self.targeted_player, team=author_team,
                                                   merkato_session=self.merkato_bid_session, type='PA',
                                                   min_price=0.1)

        bidder_1 = models.Team.objects.create(name='BIDDER1', league=self.league, division=self.division,
                                              attributes='')
        bidder_2 = models.Team.objects.create(name='BIDDER2', league=self.league, division=self.division,
                                              attributes='')
        auction_1 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_1, value='5.1')
        auction_2 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_2, value='13.1')
        auction_3 = models.Auction.objects.create(sale=sale_to_solve, team=author_team, value='13.1')
        sale_to_solve.auctions.add(auction_1, auction_2, auction_3)

        solved = auctions.solve_sale(sale_to_solve)

        self.assertIsNotNone(solved.winning_auction)
        self.assertNotEquals(solved.winning_auction.pk, auction_1.pk)
        print('%s has won' % solved.winning_auction.team.name)

    def test_not_same_player_in_session(self):
        author_team = models.Team.objects.create(name='PAMAKER', league=self.league, division=self.division,
                                                 attributes='')
        sale_to_solve = models.Sale.objects.create(player=self.targeted_player, team=author_team,
                                                   merkato_session=self.merkato_bid_session, type='PA',
                                                   min_price=0.1)
        with self.assertRaises(dbutils.IntegrityError):
            sale_that_will_fail = models.Sale.objects.create(player=self.targeted_player, team=author_team,
                                                             merkato_session=self.merkato_bid_session, type='PA',
                                                             min_price=0.1)

    def test_solve_session(self):
        for i in range(4):
            t = models.Team.objects.create(name='PAMAKER%d' % i, league=self.league, division=self.division,
                                           attributes='')
            p = l1models.Joueur.objects.create(nom='BAMOUG%d' % i, poste='A',
                                               sn_person_uuid=uuid.uuid4())

            sale_to_solve = models.Sale.objects.create(player=p, team=t,
                                                       merkato_session=self.merkato_bid_session, type='PA',
                                                       min_price=0.1)
            sale_to_solve.auctions.add(models.Auction.objects.create(sale=sale_to_solve, team=t, value=1.0))
        self.merkato_bid_session.refresh_from_db()
        with self.assertRaises(auctions.SaleSolvingException):  # closing time too early
            auctions.solve_session(self.merkato_bid_session)
        self.merkato_bid_session.closing = '2016-01-01 10:00'
        self.merkato_bid_session.save()
        self.merkato_bid_session.refresh_from_db()
        solved = auctions.solve_session(self.merkato_bid_session)
        for sale in solved.sale_set.all():
            self.assertIsNotNone(sale.winning_auction)
        self.assertTrue(solved.is_solved)