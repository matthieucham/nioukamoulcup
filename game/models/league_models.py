from django.db import models


class League(models.Model):
    MODES = (('KCUP', 'Kamoulcup'), ('FSY', 'Fantasy'))
    name = models.CharField(max_length=100)
    official = models.BooleanField(default=False)
    mode = models.CharField(max_length=4, choices=MODES)


class LeagueDivision(models.Model):
    league = models.ForeignKey(League, null=False)
    level = models.PositiveSmallIntegerField(null=False)
    name = models.CharField(max_length=100, null=False)
    capacity = models.PositiveSmallIntegerField()
    upper_division = models.ForeignKey("self")
    lower_division = models.ForeignKey("self")


