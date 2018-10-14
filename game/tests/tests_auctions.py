from django.utils import timezone
from game.models import Team, Merkato, LeagueInstance, League, LeagueDivision, MerkatoSession, Auction, Sale, Signing, \
    BankAccount
from ligue1.models import Saison, Joueur
from game.services import auctions
import uuid
from django.test import TestCase


class TestAuctions(TestCase):
    def setUp(self):
        self.league = League.objects.create(
            name='test',
            mode='KCUP',
        )
        self.division = LeagueDivision.objects.create(league=self.league, level=1, name='Test division 1',
                                                      capacity=20)
        self.merkato = Merkato.objects.create(mode='BID', begin=timezone.now(), end=timezone.now(),
                                              league_instance=LeagueInstance.objects.create(
                                                  name='test',
                                                  slogan='test',
                                                  league=self.league,
                                                  begin=timezone.now(),
                                                  end=timezone.now(),
                                                  saison=Saison.objects.create(
                                                      nom='test',
                                                      sn_instance_uuid=uuid.uuid4(),
                                                      debut=timezone.now().date(),
                                                      fin=timezone.now().date()
                                                  )
                                              ))
        self.teams = []
        for i in range(5):
            t = Team.objects.create(name='team%d' % i, league=self.league, division=self.division)
            self.teams.append(
                t
            )
        self.joueurs = [Joueur.objects.create(prenom='a', nom='A', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='b', nom='B', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='c', nom='C', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='d', nom='D', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='e', nom='E', surnom='', sn_person_uuid=uuid.uuid4(), poste='M')]

    def init_sale(self, player=None, author=None, session=None, type='PA', min_price=0.1):
        if player is None:
            player = Joueur.objects.create(prenom='b', nom='B', sn_person_uuid=uuid.uuid4(), poste='M')
        if author is None:
            author_team = Team.objects.create(name='PAMAKER', league=self.league, division=self.division,
                                              attributes='')
        if session is None:
            merkato_session = MerkatoSession.objects.create(
                merkato=self.merkato,
                number=1,
                closing=timezone.now(),
                solving=timezone.now(),
            )
        return Sale.objects.create(player=player, team=author_team,
                                   merkato_session=merkato_session, type=type,
                                   min_price=min_price)

    def init_bidder(self, team=None, balance=100):
        if team is None:
            bidder = Team.objects.create(name='BIDDER1', league=self.league, division=self.division)
        else:
            bidder = team
        BankAccount.objects.init_account(timezone.now().date(), bidder, balance, self.merkato)
        return bidder

    def set_auctions(self, sale_to_solve, bidders):
        for bidder, value in bidders:
            auction_1 = Auction.objects.create(sale=sale_to_solve, team=bidder, value=value)
            sale_to_solve.auctions.add(auction_1)
        return sale_to_solve

    def test_pa_nominal_3_auctions(self):
        author_team = Team.objects.create(name='PAMAKER', league=self.league, division=self.division)
        BankAccount.objects.init_account(timezone.now().date(), author_team, 100, self.merkato)
        merkato_session = MerkatoSession.objects.create(
            merkato=self.merkato,
            number=1,
            closing=timezone.now(),
            solving=timezone.now(),
        )
        sale_to_solve = Sale.objects.create(player=self.joueurs[0], team=author_team,
                                            merkato_session=merkato_session, type='PA',
                                            min_price=0.1)

        bidder_1 = self.teams[0]
        bidder_2 = self.teams[1]
        bidder_3 = self.teams[2]
        for b in (bidder_1, bidder_2, bidder_3):
            BankAccount.objects.init_account(timezone.now().date(), b, 100, self.merkato)
        auction_1 = Auction.objects.create(sale=sale_to_solve, team=bidder_1, value='5.1')
        auction_2 = Auction.objects.create(sale=sale_to_solve, team=bidder_2, value='4.2')
        auction_3 = Auction.objects.create(sale=sale_to_solve, team=bidder_3, value='3.4')
        sale_to_solve.auctions.add(auction_1, auction_2, auction_3)

        solved = auctions.solve_session(merkato_session)

        self.assertTrue(Auction.objects.get(pk=auction_1.pk).is_valid)
        self.assertTrue(Auction.objects.get(pk=auction_2.pk).is_valid)
        self.assertTrue(Auction.objects.get(pk=auction_3.pk).is_valid)
        self.assertEqual(solved.sale_set.get(player=self.joueurs[0]).winning_auction.pk, auction_1.pk)

        auctions.apply_transfers(merkato_session)

        s = Signing.objects.get(player=self.joueurs[0])
        self.assertEqual(s.team, auction_1.team)

    def test_pa_nominal_no_auction(self):
        sale_to_solve = self.init_sale()
        solved = auctions.solve_sale(sale_to_solve)
        self.assertIsNone(solved.winning_auction)

    def test_pa_nominal_3_auctions_with_equality(self):
        sale_to_solve = self.init_sale()
        bidder_1 = self.init_bidder()
        bidder_2 = self.init_bidder()
        author_team = self.init_bidder(team=sale_to_solve.team)

        sale_to_solve = self.set_auctions(sale_to_solve, ((bidder_1, 5.1), (bidder_2, 13.1), (author_team, 13.1)))

        solved = auctions.solve_sale(sale_to_solve)

        self.assertIsNotNone(solved.winning_auction)
        self.assertNotEquals(solved.winning_auction.pk, sale_to_solve.auctions.get(team=bidder_1))

    def test_solve_session_before_solving_time(self):
        st = timezone.now() + timezone.timedelta(days=1)
        session = MerkatoSession.objects.create(
            merkato=self.merkato,
            number=1,
            closing=timezone.now(),
            solving=st,
        )
        with self.assertRaises(auctions.SaleSolvingException):  # solving time too early
            auctions.solve_session(session)

    def test_pa_invalid_auction(self):
        sale_to_solve = self.init_sale(min_price=2.2)
        author_team = self.init_bidder(sale_to_solve.team)
        bidder_1 = self.init_bidder()
        bidder_2 = self.init_bidder()

        sale_to_solve = self.set_auctions(sale_to_solve, ((bidder_1, 5.1), (bidder_2, 101), (author_team, 2.2)))

        solved = auctions.solve_sale(sale_to_solve)

        self.assertTrue(sale_to_solve.auctions.get(team=bidder_1).is_valid)
        self.assertFalse(sale_to_solve.auctions.get(team=bidder_2).is_valid)
        self.assertEqual(sale_to_solve.auctions.get(team=bidder_2).reject_cause, 'MONEY')
        self.assertFalse(sale_to_solve.auctions.get(team=author_team).is_valid)
        self.assertEqual(sale_to_solve.auctions.get(team=author_team).reject_cause, 'MIN_PRICE')
        self.assertEqual(solved.winning_auction.pk, sale_to_solve.auctions.get(team=bidder_1).pk)
