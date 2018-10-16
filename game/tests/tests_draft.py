from django.utils import timezone
from game.models import Team, Merkato, LeagueInstance, League, DraftSession, DraftSessionRank, DraftPick, Sale, \
    MerkatoSession
from ligue1.models import Saison, Joueur
from game.services import auctions
import uuid
from django.test import TestCase


class TestDraft(TestCase):

    def setUp(self):

        self.merkato = Merkato.objects.create(mode='DRFT', begin=timezone.now(), end=timezone.now(),
                                              configuration={'default_score_factor': 1.00},
                                              league_instance=LeagueInstance.objects.create(
                                                  name='test',
                                                  slogan='test',
                                                  league=League.objects.create(
                                                      name='test',
                                                      mode='KCUP',
                                                  ),
                                                  begin=timezone.now(),
                                                  end=timezone.now(),
                                                  saison=Saison.objects.create(
                                                      nom='test',
                                                      sn_instance_uuid=uuid.uuid4(),
                                                      debut=timezone.now().date(),
                                                      fin=timezone.now().date()
                                                  )
                                              ))
        self.draft_session = DraftSession.objects.create(
            merkato=self.merkato,
            number=1,
            closing=timezone.now(),
        )
        self.teams = []
        for i in range(5):
            t = Team.objects.create(name='team%d' % i, )
            self.teams.append(
                t
            )
            self.draft_session_rank = DraftSessionRank.objects.create(
                team=t,
                rank=(i + 1 + 1),  # +1 pour le joueur déjà en vente
                draft_session=self.draft_session
            )
        self.joueurs = [Joueur.objects.create(prenom='a', nom='A', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='b', nom='B', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='c', nom='C', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='d', nom='D', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='e', nom='E', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='f', nom='F', surnom='', sn_person_uuid=uuid.uuid4(), poste='M')]
        # joueur E déjà en vente
        Sale.objects.create(player=self.joueurs[4], team=self.teams[0],
                            merkato_session=MerkatoSession.objects.create(merkato=self.merkato,
                                                                          number=1,
                                                                          closing=timezone.now(),
                                                                          solving=timezone.now()),
                            min_price=0.1)
        for dsr in DraftSessionRank.objects.all():
            for j in range(dsr.rank):
                DraftPick.objects.create(
                    pick_order=j + 1,
                    player=self.joueurs[j],
                    draft_session_rank=dsr
                )

    def test_solve_draft_session(self):
        auctions.solve_draft_session(self.draft_session)
        for index, t in enumerate(self.teams):
            rank = DraftSessionRank.objects.get(team=t, draft_session=self.draft_session)
            self.assertIsNotNone(rank.signing)
            if index < 4:
                self.assertEqual(self.joueurs[rank.rank - 1 - 1].pk, rank.signing.player.pk)  # -1 pour le +1 de là-haut
            else:
                self.assertEqual(self.joueurs[rank.rank - 1].pk, rank.signing.player.pk)
