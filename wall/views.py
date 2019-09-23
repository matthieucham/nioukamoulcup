from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, filters, pagination
from pydoc import locate
from wall.serializers import PostSerializer
from wall.models import Post, Group


class PostsPagination(pagination.CursorPagination):
    page_size = 5


# Create your views here.
class PostViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = PostSerializer
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']  # most recent first
    filter_backends = [filters.OrderingFilter]
    pagination_class = PostsPagination
    _perms = None

    def get_permissions(self):
        if self._perms is not None:
            return self._perms
        try:
            settings_permissions = settings.WALL.get('CUSTOM_PERMISSION_CLASSES', [])
            if settings_permissions:
                self._perms = [locate(permission)() for permission in settings_permissions]
            else:
                self._perms = [permissions.IsAuthenticatedOrReadOnly()]
        except AttributeError:
            self._perms = [permissions.IsAuthenticatedOrReadOnly()]
        return self._perms

    def get_queryset(self):
        group = get_object_or_404(Group.objects.all(), pk=self.kwargs['group'])
        return Post.objects.filter(in_reply_to__isnull=True).filter(group=group)

    def create(self, request, *args, **kwargs):
        response = super(PostViewSet, self).create(request, *args, **kwargs)
        # here may be placed additional operations for
        # extracting id of the object and using reverse()
        return self.list(request)

    def perform_create(self, serializer):
        group = get_object_or_404(Group.objects.all(), pk=self.kwargs['group'])
        serializer.save(author=self.request.user, group=group)
