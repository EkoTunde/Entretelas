from django.db import models


class Customer(models.Model):

    first_name = models.TextField(max_length=250)
    last_name = models.CharField(max_length=250)
    doc = models.IntegerField()
    tel = models.IntegerField()
    email = models.EmailField(max_length=120, unique=True)
    address_street = models.CharField(max_length=60)
    address_number = models.IntegerField()
    address_zip_code = models.IntegerField()
    address_city = models.CharField(max_length=60)
