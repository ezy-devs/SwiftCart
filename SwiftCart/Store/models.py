from django.db import models
from django.contrib.auth.models import User
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, related_name='creates_category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products_images', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=9999.99)
    new_price = models.DecimalField(decimal_places=2, max_digits=9999.99)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='addes_product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name}'
    
class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    product = models.ForeignKey(Product, related_name='product_collections', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='addes_collection', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


