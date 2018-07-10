from django import forms
from django.utils.translation import gettext as _
from ligue1.models import Saison, Journee


class StatsForm(forms.Form):
    def __init__(self, *args, saison=None, **kwargs):
        super(StatsForm, self).__init__(*args, **kwargs)
        if saison is not None:
            self.fields['nb_notes'].widget.attrs.update(
                {'min': 1, 'max': max(1, Journee.objects.filter(saison=saison).count())})

    nb_notes = forms.IntegerField(label='Nombre de notes',
                                  initial=1, show_hidden_initial=True,
                                  min_value=1,
                                  )


class PositionForm(forms.Form):
    position = forms.ChoiceField(label='Poste',
                                 required=False,
                                 choices=((None, 'Tous'), ('G', _('G')), ('D', _('D')), ('M', _('M')), ('A', _('A')),)
                                 )
