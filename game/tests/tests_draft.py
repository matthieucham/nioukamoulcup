from django.utils import timezone
from game.models import Team, Merkato, LeagueInstance, League, DraftSession, DraftSessionRank, DraftPick
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
                rank=(i + 1),
                draft_session=self.draft_session
            )
        self.joueurs = [Joueur.objects.create(prenom='a', nom='A', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='b', nom='B', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='c', nom='C', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='d', nom='D', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='e', nom='E', surnom='', sn_person_uuid=uuid.uuid4(), poste='M')]
        for dsr in DraftSessionRank.objects.all():
            for j in range(dsr.rank):
                DraftPick.objects.create(
                    pick_order=j + 1,
                    player=self.joueurs[j],
                    draft_session_rank=dsr
                )

    def test_solve_draft_session(self):
        auctions.solve_draft_session(self.draft_session)
        for t in self.teams:
            rank = DraftSessionRank.objects.get(team=t, draft_session=self.draft_session)
            self.assertIsNotNone(rank.signing)
            self.assertEqual(self.joueurs[rank.rank - 1].pk, rank.signing.player.pk)
