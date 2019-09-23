from rest_framework import permissions
from wall.models import Group
from game.models import League


class IsLeagueMemberOrAdmin(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        try:
            group_pk = request.parser_context['kwargs'].get('group')
            if group_pk:
                group = Group.objects.prefetch_related('league__members').get(pk=group_pk)
            else:
                return False
        except Group.DoesNotExist:
            return False
        if request.user.is_superuser:
            return True
        try:
            request.user in group.league.members.all()
            return True
        except League.DoesNotExist:
            return False
