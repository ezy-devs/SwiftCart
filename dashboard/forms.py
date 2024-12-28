# from django.contrib.auth import forms
from django import forms
from Store.models import Product, Category
from payment.models import Order, OrderItem


INPUT_CLASSES = 'input'

class CreateProductForm(forms.ModelForm):
    class Meta:

        model = Product
        fields = ('category', 'name', 'image', 'description',  'price', 'is_sale', 'sale_price', 'is_featured', 'is_trending', 'is_best_seller')

        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            # 'is_sale': forms.BooleanField(attrs={
            #     'class': INPUT_CLASSES,
            # }),
            'sale_price': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            # 'is_featured':forms.BooleanField(attrs={
            #     'class': INPUT_CLASSES,
            # }),
        }


class EditProductForm(forms.ModelForm):
    class Meta:

        model = Product
        fields = ('category', 'name', 'image', 'description',  'price', 'is_sale', 'sale_price', 'is_featured', 'is_trending', 'is_best_seller')

        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES,
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES,
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES,
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            # 'is_sale': forms.BooleanField(attrs={
            #     'class': INPUT_CLASSES,
            # }),
            'sale_price': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
            }),
            # 'is_featured':forms.BooleanField(attrs={
            #     'class': INPUT_CLASSES,
            # }),
        }


class EditOrderForm(forms.ModelForm):
    class Meta:

        model = Order
        fields = ('__all__')

class EditOrderItemForm(forms.ModelForm):
    class Meta:

        model = OrderItem
        fields = ('__all__')
