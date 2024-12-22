from django.contrib import admin
from .models import Category, Product, Collection, CollectionItem

class CollectionItemInline(admin.TabularInline):
    model = CollectionItem
    extra = 1

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CollectionItemInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_sale', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'is_sale')
    search_fields = ('name', 'description')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)

# The admin.py file is where you register your models with the Django admin site.   