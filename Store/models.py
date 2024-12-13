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
    in_stock = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10000, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
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


