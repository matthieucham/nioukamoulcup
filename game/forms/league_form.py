from django import forms
from game.services import auctions
from decimal import Decimal
from ligue1.models import Joueur


class RegisterPaForm(forms.Form):
    picked_id = forms.IntegerField()
    amount = forms.FloatField()

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.team = kwargs.pop('team')
        self.merkato = kwargs.pop('merkato')
        super(RegisterPaForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        try:
            assert Decimal(self.cleaned_data.get('amount')) > 0
            assert self.team.bank_account.balance >= Decimal(self.cleaned_data.get('amount'))
        except AssertionError:
            raise forms.ValidationError('Montant invalide', code='invalid')
        if not auctions.can_register_pa(self.team, self.merkato):
            raise forms.ValidationError('Impossible de déposer une PA', code='forbidden')

    def clean_picked_id(self):
        joueur = Joueur.objects.get(pk=self.cleaned_data.get('picked_id'))
        try:
            assert auctions.available_for_pa(joueur, self.team.division, self.merkato.league_instance)
        except AssertionError:
            raise forms.ValidationError('Ce joueur ne peut plus être sélectionné', code="invalid")
