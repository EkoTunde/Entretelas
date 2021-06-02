from django import forms
from bootstrap_datepicker_plus import DatePickerInput
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

    date = forms.DateField(
        label="Fecha:",
        widget=DatePickerInput(options={
            "format": "DD/MM/YYYY",  # moment date-time format
            "showClose": True,
            "showClear": True,
            "showTodayButton": True,
        })
    )
    method = forms.ChoiceField(choices=Payment.METHODS)
    amount = forms.DecimalField(label_suffix=': $',)
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

    date = forms.DateField(
        label="Fecha:",
        widget=DatePickerInput(options={
            "format": "DD/MM/YYYY",  # moment date-time format
            "showClose": True,
            "showClear": True,
            "showTodayButton": True,
        })
    )
    method = forms.ChoiceField(choices=Payment.METHODS)
    amount = forms.DecimalField(label_suffix=': $')

    class Meta:
        model = Payment
        fields = [
            'date',
            'method',
            'amount',
        ]
