from decimal import Decimal
from django.db import models
from django.urls import reverse


class Product(models.Model):

    HEIGHT = 'H'
    WIDTH = 'W'
    PERIMETER = 'P'
    NONE = 'NA'
    MULTIPLIERS_CHOICES = [
        (HEIGHT, 'Largo'),
        (WIDTH, 'Ancho'),
        (PERIMETER, 'Perímetro'),
        (NONE, 'Nada'),
    ]

    name = models.CharField(max_length=150)

    # Cost
    making_cost = models.DecimalField(
        verbose_name="Costo confección",
        max_digits=50, decimal_places=2, default=0)
    making_multiplier = models.CharField(
        verbose_name="Factor medida multiplicadora costo confección",
        max_length=2, choices=MULTIPLIERS_CHOICES, default=NONE)
    making_factor = models.DecimalField(
        verbose_name="Factor costo confección",
        default=None, blank=True, null=True, max_digits=50, decimal_places=2)
    making_tolerance = models.DecimalField(
        verbose_name="Tolerancia costo confección",
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)

    # 1st Component
    material_1 = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 1",
        on_delete=models.CASCADE, default=None, blank=True, null=True,
        related_name="prod_raw_material_comp_1")
    multiplier_1 = models.CharField(
        verbose_name="Factor medida multiplicadora componente 1",
        max_length=2, choices=MULTIPLIERS_CHOICES, default=NONE)
    factor_1 = models.DecimalField(
        verbose_name="Factor componente 1",
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)
    tolerance_1 = models.DecimalField(
        verbose_name="Tolerancia componente 1",
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)

    # 2nd Component
    material_2 = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 2",
        on_delete=models.CASCADE, default=None, blank=True, null=True,
        related_name="prod_raw_material_comp_2")
    multiplier_2 = models.CharField(
        verbose_name="Factor medida multiplicadora componente 2",
        max_length=2, choices=MULTIPLIERS_CHOICES, default=NONE)
    factor_2 = models.DecimalField(
        verbose_name="Factor componente 2",
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)
    tolerance_2 = models.DecimalField(
        verbose_name="Tolerancia componente 2",
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)

    # 3rd Component
    material_3 = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 3",
        on_delete=models.CASCADE, default=None, blank=True, null=True,
        related_name="prod_raw_material_comp_3")
    multiplier_3 = models.CharField(
        verbose_name="Factor medida multiplicadora componente 3",
        max_length=2, choices=MULTIPLIERS_CHOICES, default=NONE)
    factor_3 = models.DecimalField(
        verbose_name="Factor componente 3",
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)
    tolerance_3 = models.DecimalField(
        verbose_name="Tolerancia componente 3",
        default=None, blank=True, null=True,
        max_digits=50, decimal_places=2)

    def dictify(self, component, multiplier, factor, tolerance):
        return {
            'cost': Decimal(component),
            'multiplier': multiplier,
            'factor': factor,
            'tolerance': tolerance,
        }

    def components_as_dicts(self):
        result = []

        making = self.dictify(
            self.making_cost, self.making_multiplier,
            self.making_factor, self.making_tolerance)
        result.append(making)

        if self.material_1 is not None:
            comp_1 = self.dictify(
                self.material_1.price, self.multiplier_1,
                self.factor_1, self.tolerance_1)
            result.append(comp_1)

        if self.material_2 is not None:
            comp_2 = self.dictify(
                self.material_2.price, self.multiplier_2,
                self.factor_2, self.tolerance_2)
            result.append(comp_2)

        if self.material_3 is not None:
            comp_3 = self.dictify(
                self.material_3.price, self.multiplier_3,
                self.factor_3, self.tolerance_3)
            result.append(comp_3)

        return result

    def get_component_total(self, component: dict, measures: dict):
        cost = Decimal(component['cost'])

        mult_by = component['multiplier']
        if mult_by is self.NONE:
            return cost

        factor = Decimal(component['factor'])
        measure = Decimal(measures[mult_by])

        if factor == 1:
            return cost * measure

        tolerance = Decimal(component['tolerance'])
        times_it_fits = Decimal(int(measure/factor))

        reminder = Decimal(measure) - Decimal(times_it_fits * factor)
        percent_reminder = reminder * Decimal(100) / factor

        if percent_reminder > tolerance:
            times_it_fits += 1
        return cost * times_it_fits

    def get_price(self, width, height):
        total = Decimal(0)
        for component in self.components_as_dicts():
            subtotal = self.get_component_total(
                component, self.get_measures_dict(width, height))
            total += subtotal
        return total

    def get_perimeter(self, width, height):
        return (width * Decimal(2)) + (height * Decimal(2))

    def get_measures_dict(self, width, height):
        return {
            self.HEIGHT: height,
            self.WIDTH: width,
            self.PERIMETER: self.get_perimeter(width, height),
            self.NONE: Decimal(0)
        }

    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"id": self.id})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
