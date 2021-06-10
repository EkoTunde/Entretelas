from django import forms
from .models import Account


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'username',
            'first_name',
            'last_name',
        ]
