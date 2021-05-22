from django import forms

from .models import Cost


class CostModelForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = [
            'name',
            'price',
            'category',
        ]
