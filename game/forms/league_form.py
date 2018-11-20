from django import forms
from django.utils import timezone
from game.services import auctions
from decimal import Decimal
from ligue1.models import Joueur
from game.models import BankAccount, Sale, Auction, Merkato


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
            assert Decimal('%f' % self.cleaned_data.get('amount')) > 0
            assert Decimal('%f' % self.cleaned_data.get('amount')) <= 100.0
        except AssertionError:
            raise forms.ValidationError('Montant invalide', code='invalid')
        return Decimal('%f' % self.cleaned_data.get('amount'))

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
            assert self.team.bank_account.get_available() >= amount
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
            raise forms.ValidationError(
                'Le joueur %s ne peut plus être mis en vente' % Joueur.objects.get(pk=joueur_pk).display_name())
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
            raise forms.ValidationError(
                'Le joueur %s ne peut plus être mis en vente' % Joueur.objects.get(pk=joueur_pk).display_name())
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
            self.fields['_offer_for_sale__%s' % s.pk] = forms.DecimalField(
                min_value=(Decimal(s.min_price + Decimal('0.1')) if s.type == 'PA' else s.min_price),
                decimal_places=1,
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


class RegisterDraftChoicesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team')
        self.draft_session = kwargs.pop('draft_session')
        super(RegisterDraftChoicesForm, self).__init__(*args, **kwargs)
        for rk in range(self.draft_session.draftsessionrank_set.get(team=self.team).rank):
            self.fields['_pick_for_rank__%s' % (rk + 1)] = forms.IntegerField(
                required=True
            )

    def clean(self):
        # Règles à vérifier:
        # - c'est pas trop tard !
        # - que des choix différents
        # - que des joueurs libres
        # - autant de choix que son rang
        try:
            assert self.draft_session.closing >= timezone.now()
        except AssertionError:
            raise forms.ValidationError('Draft terminée, trop tard.')
        jpk = [val for field, val in self.cleaned_data.items() if field.startswith('_pick_for_rank__') and val > 0]
        try:
            assert len(jpk) == len(set(jpk))
        except AssertionError:
            raise forms.ValidationError('Certains joueurs sont choisis plusieurs fois')
        # try:
        #     assert len(jpk) == self.draft_session.draftsessionrank_set.get(team=self.team).rank
        # except AssertionError:
        #     raise forms.ValidationError('Il faut enregistrer autant de choix que son rang à la draft')
        for pk in jpk:
            try:
                assert auctions.available_for_pa(Joueur.objects.get(pk=pk), self.team.division,
                                                 self.draft_session.merkato.league_instance)
            except AssertionError:
                raise forms.ValidationError(
                    'Le joueur %s ne peut plus être sélectionné' % Joueur.objects.get(pk=pk).display_name())


class RegisterCoverForm(forms.Form):
    cover_url = forms.CharField()


class ReleaseSigningForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop('team')
        self.signing = kwargs.pop('signing')
        self.request = kwargs.pop('request')
        super(ReleaseSigningForm, self).__init__(*args, **kwargs)

    def clean(self):
        # Règles :
        # - write + release permissions
        # - signing pas déjà released
        # - signing pas locké
        try:
            assert self.team.has_object_write_permission(self.request) and self.team.has_object_release_permission(
                self.request)
        except AssertionError:
            raise forms.ValidationError('Vous n''avez pas la permission')
        try:
            assert (not self.signing.attributes.get('ending', False)) and (
                        self.signing.attributes.get('end', None) is None)
        except AssertionError:
            raise forms.ValidationError('Joueur déjà revendu')
        try:
            assert not self.signing.attributes.get('locked', False)
        except AssertionError:
            raise forms.ValidationError('Impossible de revendre ce joueur')
        try:
            assert Merkato.objects.find_current_open_merkato_for_release(self.team)
        except AssertionError:
            raise forms.ValidationError('Plus de revente possible')

