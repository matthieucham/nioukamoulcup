from django import forms
from game.models.league_models import Team
from game.models.invitation_models import TeamInvitation


class CreateTeamForm(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = Team
        fields = ('name',)


class JoinTeamForm(forms.Form):
    code = forms.CharField(max_length=38, required=True)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            TeamInvitation.objects.filter(status='OPENED').get(code=code)
        except TeamInvitation.DoesNotExist:
            raise forms.ValidationError('Ce code est inconnu')
