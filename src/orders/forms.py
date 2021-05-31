from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from django.forms.widgets import TextInput
from .models import Order, Item, Fabric, Payment


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_first_name',
            'customer_last_name',
            'customer_email',
            'customer_tel',
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

    order = forms.Field(required=True, disabled=True)
    amount = forms.DecimalField(label_suffix=': $', widget=TextInput())
    date = forms.DateField(
        label="Fecha:",
        widget=DatePickerInput(format='%d/%m/%Y')
    )

    class Meta:
        model = Payment
        fields = [
            'amount',
            'date',
            'order',
        ]


class PaymentUpdateForm(forms.ModelForm):

    amount = forms.DecimalField(label_suffix=': $')
    date = forms.DateField(
        label="Fecha:",
        widget=DatePickerInput(format='%d/%m/%Y')
    )

    class Meta:
        model = Payment
        fields = [
            'amount',
            'date',
        ]
