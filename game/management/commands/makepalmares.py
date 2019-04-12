from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from game import models as gamemodels
from game.rest import serializers
from ligue1 import models as l1models
import simplejson


class Command(BaseCommand):
    help = 'Fully recompute league instances palmares for finished phases'

    def add_arguments(self, parser):
        parser.add_argument('saison_id', nargs=1, type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            saison = l1models.Saison.objects.get(pk=options['saison_id'][0])
        except l1models.Saison.DoesNotExist:
            raise CommandError('Saison %s does not exist' % options['saison_id'][0])
        for instance in gamemodels.LeagueInstance.objects.filter(saison=saison):
            store_phases = []
            for ph in gamemodels.LeagueInstancePhase.objects.filter(league_instance=instance):
                ph_rest = serializers.PhaseRankingSerializer(
                    context={'expand_attributes': True, 'request': None}).to_representation(ph)
                if ph_rest["current_ranking"]["number"] == ph_rest["journee_last"]:
                    store_phases.append(simplejson.loads(
                        simplejson.dumps(ph_rest, iterable_as_array=True)))  # loads / dumps sert à consommer le yield
            score_by_id = dict()
            for phranking in store_phases:
                for plid, score in self._compute_players_score_for_phase(phranking["id"], phranking["current_ranking"][
                    "number"]).items():
                    if plid not in score_by_id:
                        score_by_id.update({plid: dict({'scores': []})})
                        score_by_id[plid]['scores'].append(dict({'phase': phranking["id"], 'score': score}))
            # Classement des joueurs
            players_qs = (
                l1models.Joueur.objects.filter(performances__rencontre__journee__saison=instance.saison)
            ).distinct().order_by('club__nom', 'nom')
            full_players_ranking = serializers.NewPlayersRankingSerializer(
                context={'scoring_map': score_by_id, 'phases': [{'id': ph['id'] for ph in store_phases}],
                         'request': None}, many=True).to_representation(players_qs)

            # ne conserver que ceux qui ont au moins un score:

            def filter_player_func(player):
                for phid, phscore in player['scores'].items():
                    if phscore is not None:
                        return True
                return False

            players_ranking = filter(filter_player_func, full_players_ranking)
            # Signings et Releases
            signings = serializers.SigningSerializer(context={'request': None}, many=True).to_representation(
                gamemodels.Signing.objects.filter(league_instance=instance).order_by('begin'))

            # Store in DB
            plm, _ = gamemodels.Palmares.objects.update_or_create(league=instance.league,
                                                                  league_instance_name=instance.name,
                                                                  defaults={'league_instance_slogan': instance.slogan,
                                                                            'league_instance_end': instance.end,
                                                                            'final_ranking': simplejson.dumps(
                                                                                store_phases, iterable_as_array=True),
                                                                            'players_ranking': simplejson.dumps(
                                                                                players_ranking,
                                                                                iterable_as_array=True),
                                                                            'signings_history': simplejson.dumps(
                                                                                signings, iterable_as_array=True)
                                                                            })
            # TeamPalmaresRanking
            gamemodels.TeamPalmaresRanking.objects.filter(palmares=plm).delete()
            for phranking in store_phases:
                for rk_div in phranking['current_ranking']['ranking_ekyps']:
                    rkpos = 1
                    division = gamemodels.LeagueDivision.objects.get(pk=rk_div['id'])
                    for tds in rk_div['ranking']:
                        if tds['is_complete']:
                            gamemodels.TeamPalmaresRanking.objects.create(
                                team=gamemodels.Team.objects.get(pk=tds['team']['id']),
                                palmares=plm,
                                division=division,
                                phase_name=phranking['name'],
                                phase_type=phranking['type'],
                                rank=rkpos
                            )
                            rkpos += 1

    def _compute_players_score_for_phase(self, phid, journee_number):
        score_by_id = dict()
        for tds in gamemodels.TeamDayScore.objects.filter(day__league_instance_phase__pk=phid,
                                                          day__journee__numero=journee_number):
            if tds.attributes and 'composition' in tds.attributes:
                for poste in ['G', 'D', 'M', 'A']:
                    for psco in tds.attributes['composition'][poste]:
                        scoval = float('%.1f' % round(psco['score'] / psco['score_factor'], 1))
                        score_by_id[psco['player']['id']] = scoval
        return score_by_id
