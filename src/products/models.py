from django.db import models


class Product(models.Model):

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
    component_1_raw_material = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 1",
        on_delete=models.CASCADE, related_name="prod_raw_material_comp_1")
    component_1_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES)
    component_1_factor = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_1_tolerance = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_2_raw_material = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 2",
        on_delete=models.CASCADE, related_name="prod_raw_material_comp_2")
    component_2_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES)
    component_2_factor = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_2_tolerance = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_3_raw_material = models.ForeignKey(
        "costs.Cost", verbose_name="Materia prima componente 3",
        on_delete=models.CASCADE, related_name="prod_raw_material_comp_3")
    component_3_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES)
    component_3_factor = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_3_tolerance = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_making_cost = models.ForeignKey(
        "costs.Cost", verbose_name="Costo confección",
        on_delete=models.CASCADE, related_name="prod_comp_making_cost")
    component_making_multiply_by = models.CharField(
        max_length=2, choices=MULTIPLIERS_CHOICES)
    component_making_factor = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
    component_making_tolerance = models.DecimalField(
        max_digits=50, decimal_places=2, default=NONE)
