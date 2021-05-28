import locale
from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


locale.setlocale(locale.LC_ALL, 'es_ar')


class Order(models.Model):

    NEW = "NE"
    WAITING_ANSWER = "ER"
    ACCEPTED = "AC"
    MAKING = "MK"
    FINISHED = "FI"
    STATES = [
        (NEW, 'Nuevo'),
        (WAITING_ANSWER, 'Esperando respuesta'),
        (ACCEPTED, 'Aceptado'),
        (MAKING, 'En confección'),
        (FINISHED, 'Terminado'),
    ]

    customer_first_name = models.CharField(
        max_length=100, verbose_name="Nombre")
    customer_last_name = models.CharField(
        max_length=100, verbose_name="Apellido",
        default=None, blank=True, null=True)
    customer_email = models.EmailField(
        max_length=254, verbose_name="Email",
        default=None, blank=True, null=True)
    customer_tel = models.CharField(
        max_length=50, verbose_name="Teléfono",
        default=None, blank=True, null=True)
    creation_date = models.DateTimeField(
        verbose_name="creation date", auto_now_add=True)
    last_edited = models.DateTimeField(
        verbose_name="Última edición", auto_now=True)
    expiration_date = models.DateField(
        verbose_name="Fecha de expiración",
        default=None, blank=True, null=True)
    state = models.CharField(
        max_length=1, choices=STATES, default=NEW,
        verbose_name="Estado")

    def get_absolute_url(self):
        return reverse("orders:order-detail", kwargs={"id": self.id})

    def get_balances(self, items, fabrics, payments):
        items_total = Decimal(0)
        for item in items:
            items_total += item.calculate_total()

        fabrics_total = Decimal(0)
        for fabric in fabrics:
            fabrics_total += fabric.total()

        payments_total = Decimal(0)
        for payment in payments:
            payment.get_amount()

        total = items_total + fabrics_total
        left_balance = total - payments_total
        return {
            'items_total': items_total,
            'fabrics_total': fabrics_total,
            'total': total,
            'payments_total': payments_total+Decimal(0),
            'left_balance': left_balance,
        }

    def __str__(self):
        return f'{self.id}-{self.creation_date}'

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class Item(models.Model):

    HEIGHT = 'AL'
    WIDTH = 'AN'
    PERIMETER = 'PE'
    NONE = 'NA'
    MULTIPLIERS_CHOICES = [
        (HEIGHT, 'Alto'),
        (WIDTH, 'Ancho'),
        (PERIMETER, 'Perímetro'),
        (NONE, 'Nada'),
    ]

    name = models.CharField(max_length=150)

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')

    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, null=False)

    width = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    height = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(9999)])

    def get_width(self):
        return Decimal(self.width)

    def get_height(self):
        return Decimal(self.height)

    def calculate_total(self):
        price = self.product.get_price(self.get_width(), self.get_height())
        return price * self.quantity

    def get_q(self):
        return f'{self.quantity} unidades'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


class Fabric(models.Model):

    name = models.CharField(max_length=250)
    price_per_size = models.DecimalField(max_digits=50, decimal_places=2)
    size = models.DecimalField(max_digits=50, decimal_places=2)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='fabrics', default=None)

    def total(self):
        pps = Decimal(self.price_per_size)
        s = Decimal(self.size)
        return pps * s

    def get_q(self):
        return f'{self.size} meters'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fabric"
        verbose_name_plural = "Fabrics"


class Payment(models.Model):
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    date = models.DateField(
        verbose_name="date", default=None)
    order = models.ForeignKey(
        "orders.Order", verbose_name="order",
        on_delete=models.CASCADE, related_name='payments')

    def get_amount(self):
        return Decimal(self.amount)

    def __str__(self):
        if self.date:
            return f'{self.date} - {self.amount}'
        return str(self.amount)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
