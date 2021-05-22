from django.db import models
from customers.models import Customer
from decimal import Decimal


class Order(models.Model):

    WAITING_ANSWER = "ER"
    ACCEPTED = "AC"
    MAKING = "MK"
    FINISHED = "FI"
    STATES = (
        (WAITING_ANSWER, 'Esperando respuesta'),
        (ACCEPTED, 'Aceptado'),
        (MAKING, 'En confección'),
        (FINISHED, 'Terminado'),
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_DEFAULT, default=None)
    creation_date = models.DateTimeField(
        verbose_name="creation date", auto_now_add=True)
    last_edited = models.DateTimeField(
        verbose_name="last edition", auto_now=True)
    fabrics = models.ManyToManyField("Fabric")
    expiration_date = models.DateField(
        verbose_name="expiration date", default=None)
    state = models.CharField(
        max_length=1, choices=STATES, default=WAITING_ANSWER)

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

    component_1_raw_material = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 1",
        on_delete=models.CASCADE, default=None,
        related_name="item_raw_material_comp_1")
    component_1_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES)
    component_1_factor = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_1_tolerance = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)

    component_2_raw_material = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 2",
        on_delete=models.CASCADE, default=None,
        related_name="item_raw_material_comp_2")
    component_2_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES)
    component_2_factor = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_2_tolerance = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)

    component_3_raw_material = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 3",
        on_delete=models.CASCADE, default=None,
        related_name="item_raw_material_comp_3")
    component_3_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES)
    component_3_factor = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_3_tolerance = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)

    making_cost = models.ForeignKey(
        "costs.Cost", verbose_name="Costo confección",
        on_delete=models.CASCADE, default=None,
        related_name="item_making_cost")
    making_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES)
    making_factor = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    making_tolerance = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)

    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def get_perimeter(self):
        w = 0 if self.width != "" else self.width
        h = 0 if self.height != "" else self.height
        return (w*2) + (h*2)

    def compenents_as_keys(self):
        return [
            {
                'raw_material': self.component_1_raw_material,
                'multiply_by': self.component_1_multiply_by,
                'factor': self.component_1_factor,
                'tolerance': self.component_1_tolerance,
            }, {
                'raw_material': self.component_2_raw_material,
                'multiply_by': self.component_2_multiply_by,
                'factor': self.component_2_factor,
                'tolerance': self.component_2_tolerance,
            }, {
                'raw_material': self.component_3_raw_material,
                'multiply_by': self.component_3_multiply_by,
                'factor': self.component_3_factor,
                'tolerance': self.component_3_tolerance,
            }, {
                'raw_material': self.making_cost,
                'multiply_by': self.making_multiply_by,
                'factor': self.making_factor,
                'tolerance': self.making_tolerance,
            },
        ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


class Fabric(models.Model):

    name = models.CharField(max_length=250)
    price_per_size = models.DecimalField(max_digits=50, decimal_places=2)
    size = models.DecimalField(max_digits=50, decimal_places=2)

    def total(self):
        pps = Decimal(self.price_per_size)
        s = Decimal(self.size)
        return pps * s

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fabric"
        verbose_name_plural = "Fabrics"


class Payment(models.Model):
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    date = models.DateField(
        verbose_name="date", default=None)
    order = models.ForeignKey("orders.Order", verbose_name="order",
                              on_delete=models.CASCADE,
                              related_name='payments')

    def __str__(self):
        if self.date:
            return f'{self.date} - {self.amount}'
        return str(self.amount)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
