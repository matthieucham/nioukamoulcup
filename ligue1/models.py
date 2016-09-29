from django.db import models
from django.contrib.postgres.fields import JSONField
import datetime
from django.utils import timezone

import dateutil.parser


class Importe(models.Model):
    derniere_maj = models.DateTimeField(null=True)

    def import_from_statnuts(self, statnuts_data, sn_client=None):
        self.derniere_maj = dateutil.parser.parse(statnuts_data['updated_at'])
        self.save()

    class Meta:
        abstract = True


class Saison(Importe):
    nom = models.CharField(max_length=100)
    sn_instance_uuid = models.UUIDField(null=False)
    debut = models.DateField()
    fin = models.DateField()

    def __str__(self):
        return self.nom

    def import_from_statnuts(self, statnuts_instance, sn_client=None):
        for step in statnuts_instance['steps']:
            defaults = {'numero': int(step['name'])}
            journee, created = Journee.objects.get_or_create(
                sn_step_uuid=step['uuid'],
                saison=self,
                defaults=defaults
            )
            step_update = dateutil.parser.parse(step['updated_at'])
            if created or journee.derniere_maj is None or step_update > journee.derniere_maj:
                journee.import_from_statnuts(sn_client.get_step(step['uuid']), sn_client)
        super(Saison, self).import_from_statnuts(statnuts_instance, sn_client)


class Journee(Importe):
    numero = models.PositiveIntegerField()
    sn_step_uuid = models.UUIDField(null=False)
    debut = models.DateField(null=True)
    fin = models.DateField(null=True)
    saison = models.ForeignKey(Saison, related_name='journees')

    def __str__(self):
        return str(self.numero)

    def import_from_statnuts(self, statnuts_step, sn_client):
        for meeting in statnuts_step['meetings']:
            rencontre, created = Rencontre.objects.get_or_create_from_statnuts(meeting)
            meeting_update = dateutil.parser.parse(meeting['updated_at'])
            if created or meeting_update > rencontre.derniere_maj:
                rencontre.import_from_statnuts(meeting, sn_client)
        super(Journee, self).import_from_statnuts(statnuts_step, sn_client)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            debut, fin = timezone.make_aware(datetime.datetime(datetime.MAXYEAR, 1, 1),
                                             timezone.get_default_timezone()), \
                         timezone.make_aware(datetime.datetime(datetime.MINYEAR,
                                                               1, 1), timezone.get_default_timezone())
            for x in (rencontre.date for rencontre in Rencontre.objects.filter(journee=self)):
                debut, fin = min(x, debut), max(x, fin)
            self.debut = debut
            self.fin = fin
        super(Journee, self).save(*args, **kwargs)


class Club(Importe):
    nom = models.CharField(max_length=100)
    sn_team_uuid = models.UUIDField(null=False)
    participations = models.ManyToManyField(Saison, related_name='participants')

    def __str__(self):
        return self.nom


class Joueur(Importe):
    POSTES = (('G', 'Gardien'), ('D', 'Défenseur'), ('M', 'Milieu'), ('A', 'Attaquant'))
    prenom = models.CharField(max_length=50, blank=True)
    nom = models.CharField(max_length=50)
    surnom = models.CharField(max_length=50, blank=True)
    sn_person_uuid = models.UUIDField(null=False)
    club = models.ForeignKey(Club, related_name='joueurs')
    poste = models.CharField(max_length=1, choices=POSTES)

    def __str__(self):
        return '%s %s (%s)' % (self.prenom, self.nom, self.surnom)


class RencontreManager(models.Manager):
    def get_or_create_from_statnuts(self, statnuts_data):
        if 'home_team_name' in statnuts_data:
            # indique le mode résumé
            ht_uuid = statnuts_data['home_team']
            ht_name = statnuts_data['home_team_name']
            at_uuid = statnuts_data['away_team']
            at_name = statnuts_data['away_team_name']
        else:
            # indique le mode détaillé
            ht_uuid = statnuts_data['home_team']['uuid']
            ht_name = statnuts_data['home_team']['name']
            at_uuid = statnuts_data['away_team']['uuid']
            at_name = statnuts_data['away_team']['name']

        dom, _ = Club.objects.get_or_create(sn_team_uuid=ht_uuid,
                                            defaults={'nom': ht_name})
        ext, _ = Club.objects.get_or_create(sn_team_uuid=at_uuid,
                                            defaults={'nom': at_name})

        defaults = {'date': dateutil.parser.parse(statnuts_data['date']),
                    'club_domicile': dom,
                    'club_exterieur': ext,
                    'resultat': {'dom': statnuts_data['home_result'], 'ext': statnuts_data['away_result']}}
        return self.get_or_create(
            sn_meeting_uuid=statnuts_data['uuid'],
            journee=Journee.objects.get(sn_step_uuid=statnuts_data[
                'step']),
            defaults=defaults
        )


class Rencontre(Importe):
    sn_meeting_uuid = models.UUIDField(null=False)
    club_domicile = models.ForeignKey(Club, null=False, related_name='recoit')
    club_exterieur = models.ForeignKey(Club, null=False, related_name='visite')
    date = models.DateTimeField()
    resultat = JSONField()
    hors_score = models.BooleanField(default=False)
    journee = models.ForeignKey(Journee, null=False, related_name='rencontres')
    objects = RencontreManager()

    def __str__(self):
        return '%s - %s' % (self.club_domicile.nom, self.club_exterieur.nom)

    def import_from_statnuts(self, statnuts_data, sn_client=None):
        meeting = sn_client.get_meeting(statnuts_data['uuid'])
        rencontre, created = Rencontre.objects.get_or_create_from_statnuts(statnuts_data)
        meeting_update = dateutil.parser.parse(meeting['updated_at'])
        # TODO import roster
        for ros in meeting['roster']:
            # joueur, _ = Joueur.objects.get_or_create(sn_joueur_uuid=ros['player']['uuid'])
            pass

    def save(self, *args, **kwargs):
        # crée une participation si pas déjà existante
        for cl in [self.club_domicile, self.club_exterieur]:
            if not cl.participations.filter(pk=self.journee.saison.pk).exists():
                cl.participations.add(self.journee.saison)
        super(Rencontre, self).save(*args, **kwargs)


class Performance(Importe):
    rencontre = models.ForeignKey(Rencontre, null=False)
    joueur = models.ForeignKey(Joueur, null=False)
    club = models.ForeignKey(Club, null=False)
    note = models.DecimalField(max_digits=4, decimal_places=2)
    bonus = models.DecimalField(max_digits=4, decimal_places=2)
    temps_de_jeu = models.PositiveSmallIntegerField()
    score_verrouille = models.DecimalField(max_digits=4, decimal_places=2)
    details = JSONField()

    def __str__(self):
        return '%s @ %s' % (self.joueur, self.rencontre)
