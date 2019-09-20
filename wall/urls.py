from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from wall import views

urlpatterns = [
    path('group/<uuid:group>/posts', views.PostViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name="wall-posts"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
