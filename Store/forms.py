from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = ['name', 'image', 'description', 'price', 'new_price', 'category']