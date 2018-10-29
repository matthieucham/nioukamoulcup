import bleach
import html.parser
import simplejson as jsonlib
from django.utils.safestring import mark_safe
from collections import defaultdict
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
    uncleaned = jsonlib.dumps(value, iterable_as_array=True, default=str)
    clean = html.parser.unescape(bleach.clean(uncleaned))
    return mark_safe(clean)


@register.inclusion_tag('game/tags/user_teams_invitation_code.html')
def user_teams_invitation_code(team):
    invite = models.TeamInvitation.objects.filter(team=team, status='OPENED', user__isnull=True).first()
    return {'invite': invite, 'team': team}


@register.inclusion_tag('game/tags/game_signings_inmyleagues.html', takes_context=True)
def signings_inmyleagues(context, player_id):
    if context.request.user and context.request.user.is_authenticated:
        signings = models.Signing.objects.filter(player__pk=player_id,
                                                 end__isnull=True,
                                                 league_instance__league__members=context.request.user,
                                                 league_instance__current=True).order_by('begin')
        signings_by_league = defaultdict(list)
        for s in signings:
            signings_by_league[s.league_instance].append(s)
        return {'signings': dict(signings_by_league)}
    else:
        return {'not_logged': True}
