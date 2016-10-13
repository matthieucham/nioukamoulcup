# Inside custom tag - is_active.py
from django.template import Library
register = Library()


@register.simple_tag
def is_navbar_active(request, token):
    # Main idea is to check if the url and the current path is a match
    if token in request.path:
        return "active"
    return ""