from django.db import models
from django.urls import reverse


class Cost(models.Model):

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=50, decimal_places=2)

    def get_absolute_url(self):
        return reverse("costs:cost-detail", kwargs={"id": self.id})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cost"
        verbose_name_plural = "Costs"
