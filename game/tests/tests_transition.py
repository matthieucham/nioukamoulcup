from django.utils import timezone
from game.models import Team, Merkato, LeagueInstance, League, TransitionSession, TransitionTeamChoice, Signing, \
    LeagueInstancePhase, LeagueInstancePhaseDay, TeamDayScore
from ligue1.models import Saison, Joueur, Journee
from game.services import auctions
import uuid
from collections import defaultdict
from django.test import TestCase


class TestTransition(TestCase):

    def setUp(self):

        self.merkato = Merkato.objects.create(mode='TRS', begin=timezone.now(), end=timezone.now(),
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
        self.transition_session = TransitionSession.objects.create(
            merkato=self.merkato,
            closing=timezone.now(),
        )
        self.phase = LeagueInstancePhase.objects.create(
            league_instance=self.merkato.league_instance,
            name='phtest',
            type='FULLSEASON',
            journee_first=1,
            journee_last=7
        )

        self.day = LeagueInstancePhaseDay.objects.create(
            league_instance_phase=self.phase,
            number=1,
            journee=Journee.objects.create(numero=1, sn_step_uuid=uuid.uuid4(),
                                           saison=self.merkato.league_instance.saison)
        )

        self.team = Team.objects.create(name='teamtrans', league=self.merkato.league_instance.league)
        self.joueurs = [Joueur.objects.create(prenom='a', nom='A', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='b', nom='B', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='c', nom='C', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='d', nom='D', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='e', nom='E', surnom='', sn_person_uuid=uuid.uuid4(), poste='M'),
                        Joueur.objects.create(prenom='f', nom='F', surnom='', sn_person_uuid=uuid.uuid4(), poste='M')]
        compo = defaultdict(list)
        for j in self.joueurs:
            Signing.objects.create(player=j,
                                   team=self.team,
                                   league_instance=self.merkato.league_instance)
            compo[j.poste].append({'player': {'id': j.id}, 'score': 85.0})
        TeamDayScore.objects.create(day=self.day, team=self.team, score=170.0, attributes={'composition': compo})

    def test_solve_transition_session_no_choice(self):
        auctions.solve_transition_session(self.transition_session)
        for sg in Signing.objects.filter(team=self.team, end__isnull=True):
            self.assertTrue(sg.attributes.get('locked'))
        self.assertEqual(self.transition_session.attributes.get('to_keep'),
                         Signing.objects.filter(team=self.team, end__isnull=True).count())
        for sg in Signing.objects.filter(team=self.team, end__isnull=False):
            self.assertEqual('FR', sg.attributes.get('end_reason'))
