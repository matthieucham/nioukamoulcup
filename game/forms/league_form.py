from django import forms
from game.services import auctions
from decimal import Decimal
from ligue1.models import Joueur
from game.models import BankAccount, Sale, Auction


class PickedPlayerValidationMixin:

    def clean_picked_id(self):
        joueur = Joueur.objects.get(pk=self.cleaned_data.get('picked_id'))
        try:
            assert auctions.available_for_pa(joueur, self.get_division(), self.get_league_instance())
        except AssertionError:
            raise forms.ValidationError('Ce joueur ne peut plus être sélectionné', code="invalid")
        return joueur.pk


class BaseRegisterForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.team = kwargs.pop('team')
        self.merkato = kwargs.pop('merkato')
        super(BaseRegisterForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        try:
            assert Decimal(self.cleaned_data.get('amount')) > 0
            assert Decimal(self.cleaned_data.get('amount')) <= 100.0
        except AssertionError:
            raise forms.ValidationError('Montant invalide', code='invalid')
        return Decimal(self.cleaned_data.get('amount'))

    def clean_picked_id(self):
        try:
            joueur = Joueur.objects.get(pk=self.cleaned_data.get('picked_id'))
        except Joueur.DoesNotExist:
            raise forms.ValidationError('Joueur inconnu')
        return joueur.pk


class RegisterPaForm(BaseRegisterForm):
    picked_id = forms.IntegerField()
    amount = forms.FloatField()

    def clean_amount(self):
        amount = super(RegisterPaForm, self).clean_amount()
        try:
            assert self.team.bank_account.balance >= amount
        except AssertionError:
            raise forms.ValidationError('Montant de PA trop élevé', code='too_high')
        except BankAccount.DoesNotExist:
            pass  # TODO just for testing during dev
        if not auctions.can_register_pa(self.team, self.merkato):
            raise forms.ValidationError('Impossible de déposer une PA', code='forbidden')
        return amount

    def clean_picked_id(self):
        joueur_pk = super(RegisterPaForm, self).clean_picked_id()
        try:
            assert auctions.available_for_pa(Joueur.objects.get(pk=joueur_pk), self.team.division,
                                             self.merkato.league_instance)
        except AssertionError:
            raise forms.ValidationError('Ce joueur ne peut plus être sélectionné', code="invalid")
        return joueur_pk


class RegisterMvForm(BaseRegisterForm):
    picked_id = forms.IntegerField()
    amount = forms.FloatField()

    def clean_amount(self):
        amount = super(RegisterMvForm, self).clean_amount()
        if not auctions.can_register_mv(self.team, self.merkato):
            raise forms.ValidationError('Impossible de déposer une MV', code='forbidden')
        return amount

    def clean_picked_id(self):
        joueur_pk = super(RegisterMvForm, self).clean_picked_id()
        try:
            assert auctions.available_for_mv(Joueur.objects.get(pk=joueur_pk), self.team,
                                             self.merkato.league_instance)
        except AssertionError:
            raise forms.ValidationError('Ce joueur ne peut plus être sélectionné', code="invalid")
        return joueur_pk


class RegisterOffersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team')
        self.merkato = kwargs.pop('merkato')
        sales = kwargs.pop('sales')
        super(RegisterOffersForm, self).__init__(*args, **kwargs)
        for s in sales:
            try:
                init_val = Auction.objects.get(sale=s.pk, team=self.team).value
            except Auction.DoesNotExist:
                init_val = None
            self.fields['_offer_for_sale__%s' % s.pk] = forms.FloatField(
                min_value=(s.min_price + Decimal(0.1)),
                required=False,
                initial=init_val
            )

    def clean(self):
        try:
            can, _ = auctions.can_register_auction(self.team, self.merkato)
            assert can
        except AssertionError:
            raise forms.ValidationError('Impossible d''enregistrer des enchères')
        spks = [int(field[len('_offer_for_sale__'):]) for field, v in self.cleaned_data.items() if v is not None]
        if Sale.objects.filter(pk__in=spks, type='MV', team=self.team).count() > 0:
            raise forms.ValidationError('Interdit d''enchérir sur sa propre MV')
