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
