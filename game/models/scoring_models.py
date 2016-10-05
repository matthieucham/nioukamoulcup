__author__ = 'mgrandrie'
from django.db import models
from ligue1 import models as l1models


class JourneeScoring(models.Model):
    STATUS_CHOICES = (('OPEN', 'Open'), ('LOCKED', 'locked'),)

    status = models.CharField(max_length=10, blank=False, default='OPEN', choices=STATUS_CHOICES)
    journee = models.ForeignKey(l1models.Journee, null=False)


class JJScore(models.Model):
    computed_at = models.DateTimeField(auto_now=True, null=False)
    journee_scoring = models.ForeignKey(JourneeScoring, null=False)
    joueur = models.ForeignKey(l1models.Joueur, null=False)
    note = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    bonus = models.DecimalField(max_digits=5, decimal_places=3, blank=False, null=False, default=0)
    compensation = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

