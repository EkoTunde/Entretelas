from django.contrib import admin
from .models import (Order, Item, Fabric, Payment)

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Fabric)
admin.site.register(Payment)
