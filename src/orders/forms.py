from django import forms
# from django.forms.widgets import DateInput
from .models import Order, Item, Fabric, Payment


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_first_name',
            'customer_last_name',
            'customer_email',
            'customer_tel',
            'customer_city',
            'customer_zip_code',
            'customer_state',
            'discount',
        ]


class ItemModelForm(forms.ModelForm):

    order = forms.Field(required=True, disabled=True)

    class Meta:
        model = Item
        fields = [
            'order',
            'product',
            'width',
            'height',
            'quantity',
        ]


class ItemUpdateForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = [
            'product',
            'width',
            'height',
            'quantity',
        ]


class FabricModelForm(forms.ModelForm):

    order = forms.Field(required=True, disabled=True)
    price_per_size = forms.DecimalField(label_suffix=': $')

    class Meta:
        model = Fabric
        fields = [
            'name',
            'price_per_size',
            'size',
            'order',
        ]


class FabricUpdateForm(forms.ModelForm):

    price_per_size = forms.DecimalField(label_suffix=': $')

    class Meta:
        model = Fabric
        fields = [
            'name',
            'price_per_size',
            'size',
        ]


class PaymentModelForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput(
        format=('%Y-%m-%d'), attrs={
            'class': 'datepicker',
            'placeholder': 'Fecha',
            'type': 'date'}))
    method = forms.ChoiceField(label='Método de pago', choices=Payment.METHODS)
    amount = forms.DecimalField(label='Importe', label_suffix=': $',)
    order = forms.Field(required=True, disabled=True)

    class Meta:
        model = Payment
        fields = [
            'date',
            'method',
            'amount',
            'order',
        ]


class PaymentUpdateForm(forms.ModelForm):

    date = forms.DateField(widget=forms.DateInput(
        format=('%Y-%m-%d'), attrs={
            'class': 'datepicker',
            'placeholder': 'Fecha',
            'type': 'date'}))
    method = forms.ChoiceField(label='Método de pago', choices=Payment.METHODS)
    amount = forms.DecimalField(label='Importe', label_suffix=': $')

    class Meta:
        model = Payment
        fields = [
            'date',
            'method',
            'amount',
        ]
