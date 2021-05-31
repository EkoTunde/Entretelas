from django import forms

from .models import Product


class ProductModelForm(forms.ModelForm):

    making_tolerance = forms.DecimalField(
        label='Tolerancia costo confección',
        label_suffix=" (en porcentaje)",
        required=False)
    tolerance_1 = forms.DecimalField(
        label='Tolerancia componente 1',
        label_suffix=" (en porcentaje)",
        required=False)
    tolerance_2 = forms.DecimalField(
        label='Tolerancia componente 2',
        label_suffix=" (en porcentaje)",
        required=False)
    tolerance_3 = forms.DecimalField(
        label='Tolerancia componente 3',
        label_suffix=" (en porcentaje)",
        required=False)

    class Meta:
        model = Product
        fields = [
            'name',
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
