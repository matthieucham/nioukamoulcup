import bleach
import html.parser
import simplejson as jsonlib
from django.utils.safestring import mark_safe
from game import models
# Inside custom tag - is_active.py
from django.template import Library

register = Library()


@register.simple_tag
def is_navbar_active(request, token):
    # Main idea is to check if the url and the current path is a match
    if token in request.path:
        return "active"
    return ""


@register.inclusion_tag('game/tags/game_leagues_navbar_content.html', takes_context=True)
def leagues_navbar_content(context):
    leagues = models.League.objects.filter(members=context.request.user)
    return {'leagues': leagues}


@register.filter
def json(value):
    """safe jsonify filter, bleaches the json string using the bleach html tag remover"""
    uncleaned = jsonlib.dumps(value, iterable_as_array=True)
    clean = html.parser.unescape(bleach.clean(uncleaned))
    return mark_safe(clean)


@register.inclusion_tag('game/tags/user_teams_invitation_code.html')
def user_teams_invitation_code(team):
    invite = models.TeamInvitation.objects.filter(team=team, status='OPENED').first()
    return {'invite': invite, 'team': team}


@register.inclusion_tag('game/tags/user_teams_invitations_pending.html', takes_context=True)
def user_teams_invitations_pending(context):
    invitations = models.TeamInvitation.objects.filter(team__managers__user=context.request.user,
                                                       team__managers__is_team_captain=True,
                                                       status='OPENED',
                                                       user__isnull=False)  # TODO filter with user is not null
    return {'pending_invitations': invitations}
