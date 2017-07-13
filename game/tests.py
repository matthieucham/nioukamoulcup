import uuid
import datetime
import pytz
from django.test import TestCase

from game import models
from game.services import auctions
from ligue1 import models as l1models


class TransferTestCase(TestCase):
    def setUp(self):
        self.saison = l1models.Saison.objects.create(nom='Saison', sn_instance_uuid=uuid.uuid4(),
                                                     debut=datetime.date(2017, 7, 31),
                                                     fin=datetime.date(2018, 6, 1))
        self.targeted_player = l1models.Joueur.objects.create(nom='Bamougui', poste='A',
                                                              sn_person_uuid=uuid.uuid4())

        self.league = models.League.objects.create(name='Test League', mode='KCUP')
        self.instance = models.LeagueInstance.objects.create(name='Test Instance',
                                                             begin=datetime.datetime(2017, 9, 1, 9, 0, tzinfo=pytz.UTC),
                                                             end=datetime.datetime(2017, 10, 15, 9, 0, tzinfo=pytz.UTC),
                                                             configuration='{}',
                                                             league=self.league, saison=self.saison)
        self.division = models.LeagueDivision.objects.create(league=self.league, level=1, name='Test division 1',
                                                             capacity=20)
        self.merkato_bid = models.Merkato.objects.setup(self.instance, 'BID', datetime.datetime(2017, 9, 1),
                                                        datetime.datetime(2017, 10, 15), 7)
        self.merkato_bid_session = self.merkato_bid.merkatosession_set.all()[0]

    def test_pa_nominal_3_auctions(self):
        author_team = models.Team.objects.create(name='PAMAKER', league=self.league, division=self.division,
                                                 attributes='')
        models.BankAccount.objects.init_account(author_team, 100)
        sale_to_solve = models.Sale.objects.create(player=self.targeted_player, team=author_team,
                                                   merkato_session=self.merkato_bid_session, type='PA',
                                                   min_price=0.1)

        bidder_1 = models.Team.objects.create(name='BIDDER1', league=self.league, division=self.division,
                                              attributes='')
        models.BankAccount.objects.init_account(bidder_1, 100)
        bidder_2 = models.Team.objects.create(name='BIDDER2', league=self.league, division=self.division,
                                              attributes='')
        models.BankAccount.objects.init_account(bidder_2, 100)
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
        models.BankAccount.objects.init_account(author_team, 100)
        sale_to_solve = models.Sale.objects.create(player=self.targeted_player, team=author_team,
                                                   merkato_session=self.merkato_bid_session, type='PA',
                                                   min_price=0.1)

        bidder_1 = models.Team.objects.create(name='BIDDER1', league=self.league, division=self.division,
                                              attributes='')
        models.BankAccount.objects.init_account(bidder_1, 100)
        bidder_2 = models.Team.objects.create(name='BIDDER2', league=self.league, division=self.division,
                                              attributes='')
        models.BankAccount.objects.init_account(bidder_2, 100)
        auction_1 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_1, value='5.1')
        auction_2 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_2, value='13.1')
        auction_3 = models.Auction.objects.create(sale=sale_to_solve, team=author_team, value='13.1')
        sale_to_solve.auctions.add(auction_1, auction_2, auction_3)

        solved = auctions.solve_sale(sale_to_solve)

        self.assertIsNotNone(solved.winning_auction)
        self.assertNotEquals(solved.winning_auction.pk, auction_1.pk)
        print('%s has won' % solved.winning_auction.team.name)

    def test_solve_session(self):
        for i in range(4):
            t = models.Team.objects.create(name='PAMAKER%d' % i, league=self.league, division=self.division,
                                           attributes='')
            models.BankAccount.objects.init_account(t, 100)
            p = l1models.Joueur.objects.create(nom='BAMOUG%d' % i, poste='A',
                                               sn_person_uuid=uuid.uuid4())

            sale_to_solve = models.Sale.objects.create(player=p, team=t,
                                                       merkato_session=self.merkato_bid_session, type='PA',
                                                       min_price=0.1)
            sale_to_solve.auctions.add(models.Auction.objects.create(sale=sale_to_solve, team=t, value=1.0))
        self.merkato_bid_session.refresh_from_db()
        with self.assertRaises(auctions.SaleSolvingException):  # closing time too early
            auctions.solve_session(self.merkato_bid_session)
        self.merkato_bid_session.solving = datetime.datetime(2016, 9, 1, 9, 0, tzinfo=pytz.UTC)
        self.merkato_bid_session.save()
        self.merkato_bid_session.refresh_from_db()
        solved = auctions.solve_session(self.merkato_bid_session)
        for sale in solved.sale_set.all():
            self.assertIsNotNone(sale.winning_auction)
        self.assertTrue(solved.is_solved)

    def test_pa_invalid_auction(self):
        author_team = models.Team.objects.create(name='PAMAKER', league=self.league, division=self.division,
                                                 attributes='')
        models.BankAccount.objects.init_account(author_team, 100)
        sale_to_solve = models.Sale.objects.create(player=self.targeted_player, team=author_team,
                                                   merkato_session=self.merkato_bid_session, type='PA',
                                                   min_price=2.2)

        bidder_1 = models.Team.objects.create(name='BIDDER1', league=self.league, division=self.division,
                                              attributes='')
        models.BankAccount.objects.init_account(bidder_1, 100)
        bidder_2 = models.Team.objects.create(name='BIDDER2', league=self.league, division=self.division,
                                              attributes='')
        models.BankAccount.objects.init_account(bidder_2, 100)
        auction_1 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_1, value='5.1')
        auction_2 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_2, value='101')  # invalid !
        auction_3 = models.Auction.objects.create(sale=sale_to_solve, team=author_team, value='2.2')  # invalid !
        sale_to_solve.auctions.add(auction_1, auction_2, auction_3)

        solved = auctions.solve_sale(sale_to_solve)

        self.assertTrue(models.Auction.objects.get(pk=auction_1.pk).is_valid)
        self.assertFalse(models.Auction.objects.get(pk=auction_2.pk).is_valid)
        self.assertEqual(models.Auction.objects.get(pk=auction_2.pk).reject_cause, 'MONEY')
        self.assertFalse(models.Auction.objects.get(pk=auction_3.pk).is_valid)
        self.assertEqual(models.Auction.objects.get(pk=auction_3.pk).reject_cause, 'MIN_PRICE')
        self.assertEqual(solved.winning_auction.pk, auction_1.pk)

    def test_solve_session_with_release(self):
        author_team = models.Team.objects.create(name='PAMAKER', league=self.league, division=self.division,
                                                 attributes='')
        models.BankAccount.objects.init_account(author_team, 100)
        sale_to_solve = models.Sale.objects.create(player=self.targeted_player, team=author_team,
                                                   merkato_session=self.merkato_bid_session, type='PA',
                                                   min_price=2.2)

        bidder_1 = models.Team.objects.create(name='BIDDER1', league=self.league, division=self.division,
                                              attributes='')
        models.BankAccount.objects.init_account(bidder_1, 100)
        bidder_2 = models.Team.objects.create(name='BIDDER2', league=self.league, division=self.division,
                                              attributes='')
        models.BankAccount.objects.init_account(bidder_2, 100)

        release = models.Release.objects.create(
            signing=models.Signing.objects.create(player=l1models.Joueur.objects.create(nom='VIRE', poste='A',
                                                                                        sn_person_uuid=uuid.uuid4()),
                                                  team=bidder_1, attributes='{}'),
            merkato_session=self.merkato_bid_session, amount=20)

        auction_1 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_1,
                                                  value='120')  # invalid, but must  be valid after release
        auction_2 = models.Auction.objects.create(sale=sale_to_solve, team=bidder_2,
                                                  value='91')
        auction_3 = models.Auction.objects.create(sale=sale_to_solve, team=author_team, value='120')  # invalid !
        sale_to_solve.auctions.add(auction_1, auction_2, auction_3)

        self.merkato_bid_session.solving = datetime.datetime(2016, 9, 1, 9, 0, tzinfo=pytz.UTC)
        self.merkato_bid_session.save()
        self.merkato_bid_session.refresh_from_db()
        auctions.solve_session(self.merkato_bid_session)
        sale_to_solve.refresh_from_db()
        self.assertTrue(models.Auction.objects.get(pk=auction_1.pk).is_valid)
        self.assertTrue(models.Auction.objects.get(pk=auction_2.pk).is_valid)
        self.assertFalse(models.Auction.objects.get(pk=auction_3.pk).is_valid)
        self.assertEqual(models.Auction.objects.get(pk=auction_3.pk).reject_cause, 'MONEY')
        self.assertEqual(sale_to_solve.winning_auction.pk, auction_1.pk)
        self.assertEqual(models.BankAccount.objects.get(pk=bidder_1.pk).balance, 120)
        self.assertIsNotNone(models.Release.objects.get(pk=release.pk).signing.end)
        self.assertTrue(models.Release.objects.get(pk=release.pk).done)

    def test_merkato_creation(self):
        ticks = models.MerkatoManager._generate_ticks(datetime.datetime(2017, 9, 1, 9, 0, 54, tzinfo=pytz.UTC),
                                                      datetime.datetime(2017, 9, 13, 19, 00, 20, tzinfo=pytz.UTC),
                                                      ['12:00', '20:00'])
        ticks_list = [t for t in ticks]
        for tick in ticks_list:
            print(tick)
        self.assertEqual(26, len(ticks_list))
        test_date_1 = datetime.datetime(2017, 9, 1, 9, 0, tzinfo=pytz.UTC)
        tick_1 = models.MerkatoManager._find_next_tick_to_close(test_date_1, 48, ticks_list)
        self.assertEqual(pytz.timezone('UTC').localize(datetime.datetime(2017, 9, 3, 12, 0)), tick_1)

        merkato = models.Merkato.objects.setup(self.instance, 'BID', datetime.datetime(2017, 9, 1),
                                               datetime.datetime(2017, 9, 13), 7)
        for s in merkato.merkatosession_set.all():
            print(s)

    def test_valid_auctions_against_FULL(self):
        merkato = models.Merkato.objects.setup(self.instance, 'BID', datetime.datetime(2016, 9, 1),
                                               datetime.datetime(2016, 9, 1), 2)
        sessions = merkato.merkatosession_set.order_by('closing').all()
        t_full = models.Team.objects.create(name='TFULL', league=self.league, division=self.division,
                                            attributes='')
        models.BankAccount.objects.init_account(t_full, 100)
        _load_signings(t_full, 2)  # equipe full, aucune enchere valide
        t_author_1p = models.Team.objects.create(name='TAUTHOR', league=self.league, division=self.division,
                                                 attributes='')
        models.BankAccount.objects.init_account(t_author_1p, 100)
        _load_signings(t_author_1p, 1)  # une seule place libre, seule enchere valide = la PA
        t_1p = models.Team.objects.create(name='T1P', league=self.league, division=self.division,
                                          attributes='')
        models.BankAccount.objects.init_account(t_1p, 100)
        _load_signings(t_1p, 1)  # une place libre, enchre invalide après enchère gagnée
        t_free = models.Team.objects.create(name='TFREE', league=self.league, division=self.division,
                                            attributes='')  # 0 joueur
        models.BankAccount.objects.init_account(t_free, 100)
        t_full_and_release = models.Team.objects.create(name='TFULLANDRELEASE', league=self.league,
                                                        division=self.division,
                                                        attributes='')
        models.BankAccount.objects.init_account(t_full_and_release, 100)
        _load_signings(t_full_and_release, 2)
        release = models.Release.objects.create(signing=t_full_and_release.signing_set.all()[0],
                                                merkato_session=sessions[1],
                                                amount=1)  # toutes les enchres de celui la doivent etre \
        # refusées à la session 1 et acceptées à la session 2

        # Session1 : 2 ventes, une par t_free, une par t_author_1p
        s1 = _setup_sale(t_free, 'S11', sessions[0])
        s2 = _setup_sale(t_author_1p, 'S12', sessions[0])

        # Offres de t_free: toutes valides
        # 0ffres de t_author_1p: valide sur s2 seulement
        # Offres de t_1p: valide sur s1 qu'il gagne donc invalide sur s2
        # Offres de t_full: toutes invalides
        # Offres de t_full_and_release : toutes invalides
        a1 = models.Auction.objects.create(team=t_free, sale=s1, value=2)
        a2 = models.Auction.objects.create(team=t_free, sale=s2, value=2)
        a3 = models.Auction.objects.create(team=t_author_1p, sale=s1, value=6)
        a4 = models.Auction.objects.create(team=t_author_1p, sale=s2, value=8)  # winner
        a5 = models.Auction.objects.create(team=t_1p, sale=s1, value=10.1)  # winner
        a6 = models.Auction.objects.create(team=t_1p, sale=s2, value=10.1)
        a7 = models.Auction.objects.create(team=t_full, sale=s1, value=5)
        a8 = models.Auction.objects.create(team=t_full, sale=s2, value=5)
        a9 = models.Auction.objects.create(team=t_full_and_release, sale=s1, value=5)
        a10 = models.Auction.objects.create(team=t_full_and_release, sale=s2, value=5)

        # session2 : 1 vente par t_free
        s3 = _setup_sale(t_free, 'S21', sessions[1])
        a11 = models.Auction.objects.create(team=t_free, sale=s3, value=5)
        a12 = models.Auction.objects.create(team=t_full_and_release, sale=s3, value=15)  # winner
        a13 = models.Auction.objects.create(team=t_full, sale=s3, value=25)

        for sess in sessions:
            auctions.solve_session(sess)

        a1.refresh_from_db()
        a2.refresh_from_db()
        a3.refresh_from_db()
        a4.refresh_from_db()
        a5.refresh_from_db()
        a6.refresh_from_db()
        a7.refresh_from_db()
        a8.refresh_from_db()
        a9.refresh_from_db()
        a10.refresh_from_db()
        a11.refresh_from_db()
        a12.refresh_from_db()
        a13.refresh_from_db()
        s1.refresh_from_db()
        s2.refresh_from_db()
        s3.refresh_from_db()

        self.assertTrue(a1.is_valid)
        self.assertTrue(a2.is_valid)
        self.assertFalse(a3.is_valid)
        self.assertEqual(a3.reject_cause, 'FULL')
        self.assertTrue(a4.is_valid)
        self.assertTrue(a5.is_valid)
        self.assertFalse(a6.is_valid)
        self.assertEqual(a6.reject_cause, 'FULL')
        self.assertFalse(a7.is_valid)
        self.assertEqual(a7.reject_cause, 'FULL')
        self.assertFalse(a8.is_valid)
        self.assertEqual(a8.reject_cause, 'FULL')
        self.assertFalse(a9.is_valid)
        self.assertEqual(a9.reject_cause, 'FULL')
        self.assertFalse(a10.is_valid)
        self.assertEqual(a10.reject_cause, 'FULL')
        self.assertEqual(s1.winning_auction, a5)
        self.assertEqual(s2.winning_auction, a4)
        self.assertTrue(a11.is_valid)
        self.assertTrue(a12.is_valid)
        self.assertFalse(a13.is_valid)
        self.assertEqual(a13.reject_cause, 'FULL')
        self.assertEqual(s3.winning_auction, a12)


def _load_signings(team, nb):
    for i in range(nb):
        p = l1models.Joueur.objects.create(nom='AUTO%d' % i, sn_person_uuid=uuid.uuid4())
        models.Signing.objects.create(player=p, team=team, attributes='{}')


def _setup_sale(author_team, player_name, session):
    p = l1models.Joueur.objects.create(nom=player_name, sn_person_uuid=uuid.uuid4())
    return models.Sale.objects.create(player=p, team=author_team,
                                      merkato_session=session, type='PA',
                                      min_price=0.1)