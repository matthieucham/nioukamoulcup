from django import forms


class StatsForm(forms.Form):
    nb_notes = forms.IntegerField(label='Nombre minimal de notes',
                                  min_value=1, max_value=5)
