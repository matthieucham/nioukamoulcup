import uuid
from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone

from .league_models import Team, LeagueMembership, League


class BaseInvitation(models.Model):
    STATUS_CHOICES = (('OPEN', 'OPEN'),
                      ('ACCEPTED', 'ACCEPTED'),
                      ('REJECTED', 'REJECTED'))

    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='OPEN')

    class Meta:
        abstract = True


class TeamInvitation(BaseInvitation):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    @transaction.atomic
    def accept(self):
        assert self.user is not None
        LeagueMembership.objects.create(
            user=self.user,
            league=self.team.league,
            is_team_captain=False,
            team=self.team
        )
        self.status = 'ACCEPTED'
        self.save()

    def reject(self):
        self.status = 'REJECTED'
        self.save()

    def has_object_create_permission(self, request):
        return LeagueMembership.objects.filter(user=request.user, team=self.team, is_team_captain=True).count() > 0


class LeagueInvitation(BaseInvitation):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)

    def has_object_create_permission(self, request):
        return LeagueMembership.objects.filter(user=request.user, league=self.league, is_baboon=True).count() > 0

    @transaction.atomic
    def accept(self):
        assert self.team is not None
        LeagueMembership.objects.filter(
            team=self.team,
            league__isnull=True,
            date_joined=timezone.now().date(),
        ).update(league=self.league)
        self.status = 'ACCEPTED'
        self.save()

    def reject(self):
        self.status = 'REJECTED'
        self.save()
