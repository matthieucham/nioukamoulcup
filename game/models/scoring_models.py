__author__ = 'mgrandrie'
from django.utils import timezone
from django.db import models

from ligue1 import models as l1models
from game.scoring import scoring


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
        JJScore.objects.create_or_update_jjscore_from_ligue1(self)


class JJScoreManager(models.Manager):
    def create_or_update_jjscore_from_ligue1(self, journee_scoring):
        computed_club_pks = []
        bbp = None
        for r in journee_scoring.journee.rencontres.all():
            computed_club_pks.extend([r.club_domicile.pk, r.club_exterieur.pk])
            if bbp is None:
                bbp = scoring.compute_best_by_position(r)
            for perf in r.performances.all():
                note, bonus, comp = scoring.compute_score_performance(perf, bbp)
                self.update_or_create(journee_scoring=journee_scoring, joueur=perf.joueur, defaults={
                    'note': note, 'bonus': bonus, 'compensation': comp})
                # for cl in journee_scoring.journee.saison.participants:
                # if not cl.pk in computed_club_pks:
                #         # compenser scores matchs reportés ...


class JJScore(models.Model):
    computed_at = models.DateTimeField(auto_now=True, null=False)
    journee_scoring = models.ForeignKey(JourneeScoring, null=False)
    joueur = models.ForeignKey(l1models.Joueur, null=False)
    note = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    bonus = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False, default=0)
    compensation = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    objects = JJScoreManager()

