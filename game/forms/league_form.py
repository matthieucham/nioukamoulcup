from django import forms


class RegisterPaForm(forms.Form):
    picked_id = forms.IntegerField()
