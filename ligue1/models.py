from django.db import models
from django.contrib.postgres.fields import JSONField
import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import dateutil.parser
from statnuts import note_converter


class Importe(models.Model):
    derniere_maj = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class SaisonManager(models.Manager):
    def import_from_statnuts(self, statnuts_instance, sn_client, force_import=False):
        saison = self.get(sn_instance_uuid=statnuts_instance['uuid'])  # leve une exception si pas trouvé => normal
        instance_update = dateutil.parser.parse(statnuts_instance['updated_at'])
        if force_import or saison.derniere_maj is None or instance_update > saison.derniere_maj:
            for step in statnuts_instance['steps']:
                Journee.objects.import_from_statnuts(saison, sn_client.get_step(step['uuid']), sn_client)
        saison.derniere_maj = instance_update
        saison.save()


class Saison(Importe):
    nom = models.CharField(max_length=100)
    sn_instance_uuid = models.UUIDField(null=False)
    debut = models.DateField()
    fin = models.DateField()
    objects = SaisonManager()

    def __str__(self):
        return self.nom


class JourneeManager(models.Manager):
    def import_from_statnuts(self, saison, statnuts_step, sn_client, force_import=False):
        defaults = {'numero': int(statnuts_step['name'])}
        journee, created = self.get_or_create(
            sn_step_uuid=statnuts_step['uuid'],
            saison=saison,
            defaults=defaults
        )
        step_update = dateutil.parser.parse(statnuts_step['updated_at'])
        if force_import or created or journee.derniere_maj is None or step_update > journee.derniere_maj:
            for meeting in statnuts_step['meetings']:
                Rencontre.objects.import_from_statnuts(journee, sn_client.get_meeting(meeting['uuid']), sn_client)
        journee.derniere_maj = step_update
        journee.save()


class Journee(Importe):
    numero = models.PositiveIntegerField()
    sn_step_uuid = models.UUIDField(null=False)
    debut = models.DateField(null=True)
    fin = models.DateField(null=True)
    saison = models.ForeignKey(Saison, related_name='journees')
    objects = JourneeManager()

    def __str__(self):
        return str(self.numero)

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


class JoueurManager(models.Manager):
    POSTE_SORT_ORDER = {'G': 0, 'D': 1, 'M': 2, 'A': 3, None: '10'}

    def get_or_create_from_statnuts(self, statnuts_data):
        defaults = {'prenom': statnuts_data['first_name'],
                    'nom': statnuts_data['last_name'],
                    'surnom': statnuts_data['usual_name'],
                    'poste': statnuts_data['position']}
        return self.get_or_create(sn_person_uuid=statnuts_data['uuid'],
                                  defaults=defaults)

    def set_club_from_statnuts(self, joueur, statnuts_data, maj):
        for t in statnuts_data['results']:
            try:
                club = Club.objects.get(sn_team_uuid=t['uuid'])
                joueur.club = club
            except ObjectDoesNotExist:
                pass
        joueur.derniere_maj = maj
        joueur.save()


class Joueur(Importe):
    POSTES = (('G', 'Gardien'), ('D', 'Défenseur'), ('M', 'Milieu'), ('A', 'Attaquant'))
    prenom = models.CharField(max_length=50, blank=True)
    nom = models.CharField(max_length=50)
    surnom = models.CharField(max_length=50, blank=True)
    sn_person_uuid = models.UUIDField(null=False)
    club = models.ForeignKey(Club, related_name='joueurs', null=True, blank=True)
    poste = models.CharField(max_length=1, choices=POSTES, null=True)

    objects = JoueurManager()

    def __str__(self):
        return '%s %s (%s)' % (self.prenom, self.nom, self.surnom)


class RencontreManager(models.Manager):
    def import_from_statnuts(self, journee, statnuts_meeting, sn_client, force_import=False):
        rencontre, created = self._get_or_create_from_statnuts(journee, statnuts_meeting)
        meeting_update = dateutil.parser.parse(statnuts_meeting['updated_at'])
        if force_import or created or rencontre.derniere_maj is None or meeting_update > rencontre.derniere_maj:
            self._delete_and_recreate_performances(rencontre, statnuts_meeting, sn_client)

    def _get_or_create_from_statnuts(self, journee, statnuts_data):
        # if 'home_team_name' in statnuts_data:
        # # indique le mode résumé
        # ht_uuid = statnuts_data['home_team']
        # ht_name = statnuts_data['home_team_name']
        # at_uuid = statnuts_data['away_team']
        # at_name = statnuts_data['away_team_name']
        # else:
        # indique le mode détaillé
        ht_uuid = statnuts_data['home_team']['uuid']
        ht_name = statnuts_data['home_team']['short_name']
        at_uuid = statnuts_data['away_team']['uuid']
        at_name = statnuts_data['away_team']['short_name']

        dom, _ = Club.objects.get_or_create(sn_team_uuid=ht_uuid,
                                            defaults={'nom': ht_name})
        ext, _ = Club.objects.get_or_create(sn_team_uuid=at_uuid,
                                            defaults={'nom': at_name})

        defaults = {'date': dateutil.parser.parse(statnuts_data['date']),
                    'club_domicile': dom,
                    'club_exterieur': ext}
        return self.get_or_create(
            sn_meeting_uuid=statnuts_data['uuid'],
            journee=journee,
            defaults=defaults)

    def _delete_and_recreate_performances(self, rencontre, statnuts_meeting, sn_client):
        # suppr toutes les performances déjà connues : on repart à 0 pour reimporter
        Performance.objects.filter(rencontre=rencontre).delete()
        dom_or_ext = {statnuts_meeting['home_team']['uuid']: 'dom', statnuts_meeting['away_team']['uuid']: 'ext'}
        for ros in statnuts_meeting['roster']:
            joueur, created = Joueur.objects.get_or_create_from_statnuts(ros['player'])
            joueur_updated_at = dateutil.parser.parse(ros['player']['updated_at'])
            if created or joueur.derniere_maj is None or joueur.derniere_maj < joueur_updated_at:
                Joueur.objects.set_club_from_statnuts(joueur, sn_client.get_person_teams(ros['player']['uuid']),
                                                      joueur_updated_at)
            club = Club.objects.get(sn_team_uuid=ros['played_for'])
            if ros['stats'] is None:
                tps = 0  # TODO ?
            else:
                tps = ros['stats']['playtime']
                Performance.objects.create(rencontre=rencontre, joueur=joueur, club=club, temps_de_jeu=tps,
                                           details=make_performance_details(ros, dom_or_ext[ros['played_for']]))
        rencontre.resultat = make_rencontre_resultat(statnuts_meeting)
        rencontre.derniere_maj = dateutil.parser.parse(statnuts_meeting['updated_at'])
        rencontre.save()


class Rencontre(Importe):
    sn_meeting_uuid = models.UUIDField(null=False)
    club_domicile = models.ForeignKey(Club, null=False, related_name='recoit')
    club_exterieur = models.ForeignKey(Club, null=False, related_name='visite')
    date = models.DateTimeField()
    resultat = JSONField(null=True)
    journee = models.ForeignKey(Journee, null=False, related_name='rencontres')
    objects = RencontreManager()

    def __str__(self):
        return '%s - %s' % (self.club_domicile.nom, self.club_exterieur.nom)

    def save(self, *args, **kwargs):
        # crée une participation si pas déjà existante
        for cl in [self.club_domicile, self.club_exterieur]:
            if not cl.participations.filter(pk=self.journee.saison.pk).exists():
                cl.participations.add(self.journee.saison)
        super(Rencontre, self).save(*args, **kwargs)


class Performance(models.Model):
    rencontre = models.ForeignKey(Rencontre, null=False)
    joueur = models.ForeignKey(Joueur, null=False)
    club = models.ForeignKey(Club, null=False)
    temps_de_jeu = models.PositiveSmallIntegerField()
    details = JSONField()

    def __str__(self):
        return '%s @ %s' % (self.joueur, self.rencontre)


def make_rencontre_resultat(statnuts_meeting):
    dom = {'buts_pour': statnuts_meeting['home_result'], 'buts_contre': statnuts_meeting['away_result']}
    ext = {'buts_pour': statnuts_meeting['away_result'], 'buts_contre': statnuts_meeting['home_result']}
    # récupérer les penaltys
    peno_dom = 0
    peno_ext = 0
    for roster in statnuts_meeting['roster']:
        if roster['stats'] is not None and roster['stats']['penalties_scored'] is not None and roster['stats'][
            'penalties_scored'] > 0:
            if roster['played_for'] == statnuts_meeting['home_team']['uuid']:
                peno_dom += roster['stats']['penalties_scored']
            elif roster['played_for'] == statnuts_meeting['away_team']['uuid']:
                peno_ext += roster['stats']['penalties_scored']
    dom['penos_pour'] = peno_dom
    dom['penos_contre'] = peno_ext
    ext['penos_pour'] = peno_ext
    ext['penos_contre'] = peno_dom
    return {'dom': dom, 'ext': ext}


def make_performance_details(statnuts_roster, dom_or_ext):
    return {'equipe': dom_or_ext, 'stats': statnuts_roster['stats'], 'note': note_converter.compute_note(
        statnuts_roster['ratings'])}
