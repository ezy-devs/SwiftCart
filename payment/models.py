from django.db import models
from django.contrib.auth.models import User
from Store.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver




class ShippingInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_info', null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255, null=True, blank=True)
    shipping_phone_number = models.CharField(max_length=20, null=True, blank=True)
    shipping_email = models.CharField(max_length=255, null=True, blank=True)
    shipping_address_1 = models.CharField(max_length=255)
    shipping_address_2 = models.CharField(max_length=255, null=True, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20, null=True, blank=True)
    shipping_country = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipping Info for {self.user or self.session_key} - {self.shipping_address_1}, {self.shipping_city}"

@receiver(post_save, sender=User)
def create_or_update_user_shipping(sender, instance, created, **kwargs):
    if created:  # If the User instance is created
        ShippingInfo.objects.create(user=instance)
    else:  # If the User instance is updated
        instance.shipping_info


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, default='')
    shipping_address = models.CharField(max_length=255, null=True,)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_ordered = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """ Automatically set price based on product price """
        if not self.price:
            self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} - Order #{self.order.id}"



