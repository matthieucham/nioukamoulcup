from django.db import models
from django.contrib.postgres.fields import JSONField


class Importe(models.Model):
    derniere_maj = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Saison(Importe):
    nom = models.CharField(max_length=100)
    sn_instance_uuid = models.UUIDField(null=False)
    debut = models.DateField()
    fin = models.DateField()


class Journee(Importe):
    numero = models.PositiveIntegerField()
    sn_step_uuid = models.UUIDField(null=False)
    debut = models.DateField()
    fin = models.DateField()
    saison = models.ForeignKey(Saison, related_name='journees')


class Club(Importe):
    nom = models.CharField(max_length=100)
    sn_team_uuid = models.UUIDField(null=False)
    participations = models.ManyToManyField(Saison, related_name='participants')


class Joueur(Importe):
    POSTES = (('G', 'Gardien'), ('D', 'Défenseur'), ('M', 'Milieu'), ('A', 'Attaquant'))
    prenom = models.CharField(max_length=50, blank=True)
    nom = models.CharField(max_length=50)
    surnom = models.CharField(max_length=50, blank=True)
    sn_person_uuid = models.UUIDField(null=False)
    club = models.ForeignKey(Club, related_name='joueurs')
    poste = models.CharField(max_length=1, choices=POSTES)


class Rencontre(Importe):
    sn_meeting_uuid = models.UUIDField(null=False)
    club_domicile = models.ForeignKey(Club, null=False, related_name='recoit')
    club_exterieur = models.ForeignKey(Club, null=False, related_name='visite')
    date = models.DateTimeField()
    resultat = JSONField()
    hors_score = models.BooleanField(default=False)


class Performance(Importe):
    rencontre = models.ForeignKey(Rencontre, null=False)
    joueur = models.ForeignKey(Joueur, null=False)
    note = models.DecimalField(max_digits=4, decimal_places=2)
    bonus = models.DecimalField(max_digits=4, decimal_places=2)
    temps_de_jeu = models.PositiveSmallIntegerField()
    score_verrouille = models.DecimalField(max_digits=4, decimal_places=2)
    details = JSONField()
