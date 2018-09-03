from django.db import models
from zinnia.models_bases.entry import AbstractEntry
from .league_models import League


class EntryLeague(AbstractEntry):
    league = models.ForeignKey(League, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'EntryLeague %s' % self.title

    class Meta(AbstractEntry.Meta):
        abstract = True
