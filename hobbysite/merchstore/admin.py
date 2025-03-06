from django.contrib import admin
from .models import ProductType, Product

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price')
    list_filter = ('product_type',)
    search_fields = ('name', 'description')
