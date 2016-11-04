__author__ = 'mgrandrie'
from django.utils import timezone
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from ligue1 import models as l1models
from game.scoring import scoring
from utils.timer import Timer


class SaisonScoring(models.Model):
    saison = models.ForeignKey(l1models.Saison, null=False)
    computed_at = models.DateTimeField(auto_now=True)


class JourneeScoring(models.Model):
    STATUS_CHOICES = (('OPEN', 'Open'), ('LOCKED', 'locked'),)

    status = models.CharField(max_length=10, blank=False, default='OPEN', choices=STATUS_CHOICES)
    journee = models.ForeignKey(l1models.Journee, null=False)
    saison_scoring = models.ForeignKey(SaisonScoring, null=False)
    computed_at = models.DateTimeField(null=True)
    locked_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.status == 'LOCKED':
            self.computed_at = timezone.now()
        super(JourneeScoring, self).save(*args, **kwargs)
        if not self.status == 'LOCKED':
            self.compute_scores()

    def lock(self):
        self.compute_scores()
        self.status = 'LOCKED'
        self.locked_at = timezone.now()
        self.save()

    def compute_scores(self):
        JJScore.objects.create_jjscore_from_ligue1(self)


class JJScoreManager(models.Manager):
    def create_jjscore_from_ligue1(self, journee_scoring):
        with Timer(id='create_jjscore_from_ligue1', verbose=True):
            computed_club_pks = []
            bbp = None
            jjscores = []
            for r in journee_scoring.journee.rencontres.all():
                computed_club_pks.extend([r.club_domicile.pk, r.club_exterieur.pk])
                all_perfs = r.performances.select_related('joueur').select_related('rencontre').all()
                if all_perfs:  # perform queryset
                    if bbp is None:
                        bbp = scoring.compute_best_by_position(all_perfs)
                    for perf in all_perfs:
                        note, bonus, comp = scoring.compute_score_performance(perf, bbp)
                        jjscores.append(JJScore(journee_scoring=journee_scoring, joueur=perf.joueur, note=note, bonus=bonus,
                                                compensation=comp))
                        # for cl in journee_scoring.journee.saison.participants:
                        # if not cl.pk in computed_club_pks:
                        # compenser scores matchs reportés ...
            # "pour les joueurs qui n'ont pas joué lors de cette journée insert 0":
            # TODO
            JJScore.objects.filter(journee_scoring=journee_scoring).delete()
            JJScore.objects.bulk_create(jjscores)

    def list_scores_for_joueur(self, joueur, saison_scoring):
        return self.filter(joueur=joueur, journee_scoring__saison_scoring=saison_scoring).order_by(
            'journee_scoring__journee__numero')

        # raw_query = 'select ligue1_journee.id, numero, note::float, bonus::float, compensation::float, coalesce(bonus + coalesce(note,compensation), 0)::float as points from ligue1_journee inner join game_journeescoring on game_journeescoring.journee_id=ligue1_journee.id left join game_jjscore on game_jjscore.journee_scoring_id=game_journeescoring.id and game_jjscore.joueur_id=%s where ligue1_journee.saison_id=%s order by numero asc'
        # return self.raw(raw_query, [joueur.pk, saison_scoring.saison.pk])

        # jsc_map = {jsc.journee_scoring.journee.pk: jsc for jsc in JJScore.objects.filter(joueur=joueur,
        # journee_scoring__saison_scoring=saison_scoring)}
        # result = []
        # for journee in l1models.Journee.objects.filter(saison=saison_scoring.saison).order_by('numero'):
        #     if journee.pk in jsc_map:
        #         result.append(jsc_map[journee.pk])
        #     else:
        #         result.append(JJScore(journee_scoring=JourneeScoring(journee=journee, saison_scoring=saison_scoring),
        #                               joueur=joueur, note=0, bonus=0, compensation=0))
        # return result


class JJScore(models.Model):
    computed_at = models.DateTimeField(auto_now=True, null=False)
    journee_scoring = models.ForeignKey(JourneeScoring, null=False)
    joueur = models.ForeignKey(l1models.Joueur, null=False)
    note = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    bonus = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False, default=0)
    compensation = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    objects = JJScoreManager()

