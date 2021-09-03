from zinnia.views.channels import EntryChannel
from zinnia.models.entry import Entry
from django.views.generic import TemplateView

# Create your views here.


class LeagueEntryDetail(EntryChannel):

    def get_queryset(self):
        # if self.kwargs:
        #     league_pk = self.kwargs.get('pk') or None
        #     if league_pk:
        #         return Entry.published.filter(league=league_pk)
        #     else:
        #         return Entry.published.filter(league__isnull=True)
        # else:
        #     return Entry.published.filter(league__isnull=True)
        return Entry.published.all()


class LandingPageView(TemplateView):

    template_name = 'game/landing.html'
