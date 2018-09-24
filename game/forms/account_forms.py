from django import forms
from game.models.league_models import Team


class CreateTeamForm(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = Team
        fields = ('name',)
