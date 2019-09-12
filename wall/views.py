from django.apps import apps
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, filters

from wall.serializers import PostSerializer
from wall.models import Post, Group


# Create your views here.
class PostViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = PostSerializer
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']  # most recent first
    filter_backends = [filters.OrderingFilter]

    def get_permissions(self):
        try:
            settings_permissions = settings.WALL.get('CUSTOM_PERMISSION_CLASSES', [])
            if settings_permissions:
                return [permission() for permission in settings_permissions]
            else:
                return [permissions.IsAuthenticatedOrReadOnly()]
        except AttributeError:
            return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        group = get_object_or_404(Group.objects.all(), pk=self.kwargs['group'])
        return Post.objects.filter(in_reply_to__isnull=True).filter(group=group)

    # def create(self, request, *args, **kwargs):
    #     group = get_object_or_404(Group.objects.all(), pk=self.kwargs['group'])
    #     request.data['author'] = request.user.pk
    #     return super(PostViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        group = get_object_or_404(Group.objects.all(), pk=self.kwargs['group'])
        serializer.save(author=self.request.user, group=group)
