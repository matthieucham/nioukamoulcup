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

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.request = kwargs.pop('request')
        super(JoinTeamForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            invit = TeamInvitation.objects.filter(status='OPENED').get(code=code)
        except TeamInvitation.DoesNotExist:
            raise forms.ValidationError('Ce code est inconnu')
        try:
            assert invit.team.managers.filter(user=self.request.user).count() == 0
        except AssertionError:
            raise forms.ValidationError('Vous êtes déjà manager de cette équipe')
