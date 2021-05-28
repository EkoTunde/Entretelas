from django import forms

from .models import Product


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'customer_last_name',
            'customer_email',
            'customer_tel',
            'making_cost',
            'making_multiplier',
            'making_factor',
            'making_tolerance',
            'material_1',
            'multiplier_1',
            'factor_1',
            'tolerance_1',
            'material_2',
            'multiplier_2',
            'factor_2',
            'tolerance_2',
            'material_3',
            'multiplier_3',
            'factor_3',
            'tolerance_3',
        ]
