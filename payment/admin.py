from django.contrib import admin
from .models import ShippingInfo, Order, OrderItem
# Register your models here.

admin.site.register(ShippingInfo)
admin.site.register(Order)
admin.site.register(OrderItem)
