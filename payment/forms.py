from .models import ShippingInfo
from django import forms

INPUT_CLASSES = 'input'
class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ['shipping_full_name', 'shipping_email', 'shipping_phone_number', 'shipping_address_1', 'shipping_address_2', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country']

        widgets = {
            
            'shipping_full_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'shipping_email': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'shipping_phone_number': forms.TextInput(attrs={
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

class PaymentForm(forms.Form):
    card_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder': 'Card name'}))
    card_number = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder': 'card number'}))
    card_exp_date = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder': 'Expire date'}))
    card_cvv_number = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder':'cvv number'}))
    card_address1 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder':'card address 1'}))
    card_address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder':'card address 2'}))
    card_city = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder':'City'}))
    card_state = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder':'State'}))
    card_zipcode = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder':'Zip code'}))
    card_country = forms.CharField(label='', widget=forms.TextInput(attrs={'class':INPUT_CLASSES, 'placeholder':'Country'}))





class PaymentForm(forms.Form):
    email = forms.EmailField()
    amount = forms.IntegerField()