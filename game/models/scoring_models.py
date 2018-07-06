__author__ = 'mgrandrie'
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField

from ligue1 import models as l1models
# from game import models as gamemodels
from game.services import scoring
from utils.timer import Timer


class SaisonScoring(models.Model):
    saison = models.ForeignKey(l1models.Saison, on_delete=models.CASCADE, null=False)
    computed_at = models.DateTimeField(auto_now=True)

    def compute(self):
        journees = l1models.Journee.objects.filter(saison=self.saison).order_by('numero')
        journees_to_recompute = []
        # delete obsolete journeescorings
        for j in journees:
            js = JourneeScoring.objects.filter(saison_scoring=self, journee=j).first()
            if js:
                if js.computed_at < j.derniere_maj:
                    journees_to_recompute.append(j)
                    js.delete()
            else:
                journees_to_recompute.append(j)
        for journee in journees_to_recompute:
            JourneeScoring.objects.select_related('journee').create(journee=journee, saison_scoring=self)
        SJScore.objects.create_sjscore_from_ligue1(self)


class JourneeScoring(models.Model):
    STATUS_CHOICES = (('OPEN', 'Open'), ('LOCKED', 'locked'),)

    status = models.CharField(max_length=10, blank=False, default='OPEN', choices=STATUS_CHOICES)
    journee = models.ForeignKey(l1models.Journee, on_delete=models.CASCADE, null=False)
    saison_scoring = models.ForeignKey(SaisonScoring, on_delete=models.CASCADE, null=False)
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
        with Timer(id='create_jjscore_from_ligue1', verbose=False):
            computed_club_pks = []
            jjscores = []
            computed_joueurs = []
            for r in journee_scoring.journee.rencontres.all():
                computed_club_pks.extend([r.club_domicile.pk, r.club_exterieur.pk])
                all_perfs = r.performances.select_related('joueur').select_related('rencontre').all()
                bbp = None
                if all_perfs:  # perform queryset
                    if bbp is None:
                        bbp = scoring.compute_best_by_position(all_perfs)
                    for perf in all_perfs:
                        note, bonus, comp, earned_bonuses = scoring.compute_score_performance(perf, bbp)
                        jjscores.append(
                            JJScore(journee_scoring=journee_scoring, joueur=perf.joueur, rencontre=r, note=note,
                                    bonus=bonus,
                                    compensation=comp, details={'bonuses': earned_bonuses}))
                        # for cl in journee_scoring.journee.saison.participants:
                        # if not cl.pk in computed_club_pks:
                        # compenser scores matchs reportés ...
                        computed_joueurs.append(perf.joueur.pk)
            # "pour les joueurs qui n'ont pas joué lors de cette journée insert 0":
            for j in l1models.Joueur.objects.exclude(pk__in=computed_joueurs):
                jjscores.append(JJScore(journee_scoring=journee_scoring, joueur=j, compensation=0, bonus=0))
            JJScore.objects.filter(journee_scoring=journee_scoring).delete()
            JJScore.objects.bulk_create(jjscores)

    def list_scores_for_joueur(self, joueur, saison_scoring):
        return self.filter(joueur=joueur, journee_scoring__saison_scoring=saison_scoring).order_by(
            'journee_scoring__journee__numero')

    def count_notes(self, saison, joueur_ids, max_by_joueur, journee_first=None, journee_last=None):
        notes_notnull = models.Count('note')
        queryset = self.filter(joueur__in=joueur_ids, journee_scoring__saison_scoring__saison=saison,
                               note__isnull=False)
        if journee_first:
            queryset = queryset.filter(journee_scoring__journee__numero__gte=journee_first)
        if journee_last:
            queryset = queryset.filter(journee_scoring__journee__numero__lte=journee_last)
        queryset = queryset.values('joueur').annotate(notes_notnull=notes_notnull)
        return sum([min(n, max_by_joueur) for n in queryset.values_list('notes_notnull', flat=True)])

    def get_n_best_or_worst(self, journee, numberof, poste=None, best=True):
        ofjournee = self.filter(journee_scoring__journee=journee, note__isnull=False)
        if poste is not None:
            ofjournee = ofjournee.filter(joueur__poste=poste)
        if best:
            ordering = '-note'
        else:
            ordering = 'note'
        return ofjournee.order_by(ordering)[:numberof]


class JJScore(models.Model):
    computed_at = models.DateTimeField(auto_now=True, null=False)
    journee_scoring = models.ForeignKey(JourneeScoring, on_delete=models.CASCADE, null=False)
    joueur = models.ForeignKey(l1models.Joueur, on_delete=models.CASCADE, null=False)
    rencontre = models.ForeignKey(l1models.Rencontre, on_delete=models.CASCADE, null=True)
    note = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    bonus = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False, default=0)
    compensation = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    details = JSONField(default=dict())

    objects = JJScoreManager()


class SJScoreManager(models.Manager):

    def create_sjscore_from_ligue1(self, saison_scoring):
        with Timer(id='create_sjscore_from_ligue1', verbose=True):
            sjscores = []
            jjscores_by_joueur = dict()
            for jjs in JJScore.objects.select_related('joueur').filter(journee_scoring__saison_scoring=saison_scoring):
                jjscores_by_joueur.setdefault(jjs.joueur, []).append(jjs)
            for jpk, scores in jjscores_by_joueur.items():
                agglo = self._compute_stats_agg(scores)
                sjscores.append(SJScore(saison_scoring=saison_scoring,
                                        joueur=jpk,
                                        avg_note=agglo.pop('AVGNOTE'),
                                        nb_notes=agglo.pop('NBNOTE'),
                                        total_bonuses=agglo.pop('BONUS'),
                                        sum_compensations=agglo.pop('SUMCOMP'),
                                        details=agglo))
            self.filter(saison_scoring=saison_scoring).delete()
            self.bulk_create(sjscores)

    def _compute_stats_agg(self, jjscores):
        agg = dict()
        for bk in set(scoring.BONUS['COLLECTIVE'].keys()).union(set(scoring.BONUS['PERSONAL'].keys())):
            agg[bk] = 0
        for jjs in jjscores:
            for bk in set(scoring.BONUS['COLLECTIVE'].keys()).union(set(scoring.BONUS['PERSONAL'].keys())):
                if 'bonuses' in jjs.details and bk in jjs.details['bonuses']:
                    agg[bk] += jjs.details['bonuses'][bk]
        notes = [jjs.note for jjs in jjscores if jjs.note is not None]
        bonus = [jjs.bonus for jjs in jjscores if jjs.bonus is not None]
        compensations = [jjs.compensation for jjs in jjscores if jjs.compensation is not None]
        agg['AVGNOTE'] = round(sum(notes) / len(notes), 2) if len(notes) > 0 else None
        agg['NBNOTE'] = len(notes)
        agg['BONUS'] = sum(bonus)
        agg['SUMCOMP'] = sum(compensations)
        return agg


class SJScore(models.Model):
    computed_at = models.DateTimeField(auto_now=True, null=False)
    saison_scoring = models.ForeignKey(SaisonScoring, on_delete=models.CASCADE, null=False)
    joueur = models.ForeignKey(l1models.Joueur, on_delete=models.CASCADE, null=False)
    avg_note = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    nb_notes = models.PositiveIntegerField(null=False, default=0)
    total_bonuses = models.DecimalField(max_digits=6, decimal_places=3, blank=False, null=False, default=0)
    sum_compensations = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    details = JSONField(default=dict())

    objects = SJScoreManager()

    # class TeamScore(models.Model):
    # team = models.OneToOneField(gamemodels.Team, primary_key=True)
    # kcup_score = models.FloatField(default=0.0)
    #     computed_at = models.DateTimeField(auto_now_add=True)
