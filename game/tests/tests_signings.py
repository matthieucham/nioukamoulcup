from django.test import TestCase
from game.models import Team, Merkato, LeagueInstance, League, LeagueDivision, MerkatoSession, Auction, Sale, Signing, \
    BankAccount
from ligue1.models import Saison, Joueur
from game.services import auctions
from django.utils import timezone
import uuid
import decimal


class TestSignings(TestCase):
    def setUp(self):
        self.league = League.objects.create(
            name='test',
            mode='KCUP',
        )
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
        self.merkato_session = MerkatoSession.objects.create(
                merkato=self.merkato,
                number=1,
                closing=timezone.now(),
                solving=timezone.now(),
            )

        assert 're_tax_rate' in self.merkato.configuration

    def test_amount_computation(self):
        sale = Sale(merkato_session=self.merkato_session)
        # montant entier
        sale.min_price = decimal.Decimal(10)
        attr = auctions._make_signing_attr(sale)
        self.assertEqual(10, attr['amount'])
        self.assertEqual(5, attr['release_amount'])

        # montant decimal pair
        sale.min_price = decimal.Decimal(6.2)
        attr = auctions._make_signing_attr(sale)
        self.assertEqual(6.2, attr['amount'])
        self.assertEqual(3.1, attr['release_amount'])

        # montant decimal impair
        sale.min_price = decimal.Decimal(5.5)
        attr = auctions._make_signing_attr(sale)
        self.assertEqual(5.5, attr['amount'])
        self.assertEqual(2.8, attr['release_amount'])

        # montant minimal
        sale.min_price = decimal.Decimal(0.1)
        attr = auctions._make_signing_attr(sale)
        self.assertEqual(0.1, attr['amount'])
        self.assertEqual(0.1, attr['release_amount'])
