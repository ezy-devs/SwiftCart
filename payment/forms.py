from .models import ShippingInfo
from django import forms

INPUT_CLASSES = 'input'
class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ['shipping_full_name', 'shipping_phone_number', 'shipping_address_1', 'shipping_address_2', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country']

        widgets = {
            'shipping_phone_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'shipping_full_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'shipping_address_1': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'shipping_address_1': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'shipping_state': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'shipping_postal_code': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'shipping_country': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
        }
        