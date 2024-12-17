from .models import ShippingInfo
from django import forms

INPUT_CLASSES = 'input'
class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ['phone_number', 'address_1', 'address_2', 'city', 'state', 'postal_code', 'country']

        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'address_1': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'address_1': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'city': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'state': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'postal_code': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'country': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
        }
        