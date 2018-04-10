# -*- coding: utf-8 -*-
from django import forms


# PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Форма для доваления товаров в корзину"""
    # quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    quantity = forms.IntegerField(
        label='Кол-во', min_value=1, initial=1, required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity', 'min': '1', 'required': True}))
    is_update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput, help_text='был ли товар добавлен в корзину')

