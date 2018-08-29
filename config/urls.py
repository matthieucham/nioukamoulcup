"""nioukamoulcup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
#from wiki.urls import get_pattern as get_wiki_pattern
#from django_nyt.urls import get_pattern as get_nyt_pattern
from ligue1.admin_import import admin_import_site

urlpatterns = [
    url(r'^game/home/info/', include('zinnia.urls')),
    url(r'^game/', include('game.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('userena.urls')),
    url(r'^comments/', include('django_comments.urls')),
    # url(r'^notifications/', get_nyt_pattern()),
    # url(r'^wiki/', get_wiki_pattern()),
    url(r'^import/', admin_import_site.urls, name='import'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]