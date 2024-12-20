from django.contrib import admin
from django.contrib.auth.models import User

from .models import ShippingInfo, Order, OrderItem
# Register your models here.


class ShippingInfoInline(admin.StackedInline):
    model = ShippingInfo
    can_delete = False
    verbose_name_plural = 'ShippingInfo'

# Extend UserAdmin to include Profile
class UserAdmin(admin.ModelAdmin):
    inlines = [ShippingInfoInline]

# Unregister the default User admin and register the extended one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# admin.site.register(ShippingInfo)
admin.site.register(Order)
admin.site.register(OrderItem)
