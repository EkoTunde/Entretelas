from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal


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
        on_delete=models.CASCADE, default=None, blank=True, null=True,
        related_name="item_raw_material_comp_1")
    component_1_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES, default=NONE)
    component_1_factor = models.DecimalField(
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)
    component_1_tolerance = models.DecimalField(
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)

    component_2_raw_material = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 2",
        on_delete=models.CASCADE, default=None, blank=True, null=True,
        related_name="item_raw_material_comp_2")
    component_2_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES, default=NONE)
    component_2_factor = models.DecimalField(
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)
    component_2_tolerance = models.DecimalField(
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)

    component_3_raw_material = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 3",
        on_delete=models.CASCADE, default=None, blank=True, null=True,
        related_name="item_raw_material_comp_3")
    component_3_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES, default=NONE)
    component_3_factor = models.DecimalField(
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)
    component_3_tolerance = models.DecimalField(
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)

    making_cost = models.ForeignKey(
        "costs.Cost", verbose_name="Costo confección",
        on_delete=models.CASCADE, default=None, blank=True, null=True,
        related_name="item_making_cost")
    making_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES, default=NONE)
    making_factor = models.DecimalField(
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)
    making_tolerance = models.DecimalField(
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)

    width = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0))
    height = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0))
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(9999)])

    def get_height(self):
        h = 0 if self.height != "" or self.height is not None else self.height
        return Decimal(h)

    def get_width(self):
        w = 0 if self.width != "" or self.width is not None else self.width
        return Decimal(w)

    def get_perimeter(self):
        return (self.get_width()*2) + (self.get_height()*2)

    def components_as_keys(self):
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

    def calculate_total(self):
        components = self.components_as_keys()
        total = Decimal(0)
        for component in components:
            total += self.get_component_total(component)
        return total

    def get_component_total(self, comp):
        material = comp['raw_material']
        if material is None:
            return Decimal(0)

        mult_by = comp['multiply_by']
        if mult_by is self.NONE:
            return Decimal(material.price)

        factor = comp['factor']
        measure = self.get_measures()[mult_by]

        if factor == 1:
            return material.price * measure

        tolerance = comp['tolerance']
        times_it_fits = int(measure/factor)

        intolerant = measure - (times_it_fits * factor) > tolerance
        result = material * (times_it_fits+1 if intolerant else times_it_fits)
        return Decimal(result)

    def get_measures(self):
        return {
            self.WIDTH: self.get_width(),
            self.HEIGHT: self.get_height(),
            self.PERIMETER: self.get_perimeter(),
        }

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
