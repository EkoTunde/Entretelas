from django.db import models
from django.urls import reverse


class Cost(models.Model):

    MAKING = "CO"
    RAW_MATERIAL = "MP"
    CATEGORIES_CHOICES = [
        (MAKING, 'Confección'),
        (RAW_MATERIAL, 'Materia prima'),
    ]

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    category = models.CharField(max_length=2, choices=CATEGORIES_CHOICES)

    def get_absolute_url(self):
        return reverse("costs:cost-detail", kwargs={"id": self.id})

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = "Cost"
        verbose_name_plural = "Costs"
