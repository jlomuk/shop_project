from django import forms
from django.forms import NumberInput


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=NumberInput(attrs={
            'class': 'form-control text-center px-2',
            'value': 1,
            'readonly':'',
        })
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
