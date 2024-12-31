from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='', null=True, blank=True)
    user = models.ForeignKey(User, related_name='creates_category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    def get_absolute_url(self):
        return reverse('edit-category', args=[str(self.id)])
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
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('product', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.name}'
    
class Collection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='collections/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Collection, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class CollectionItem(models.Model):
    collection = models.ForeignKey(Collection, related_name='collection_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.collection.name} - {self.product.name}'
