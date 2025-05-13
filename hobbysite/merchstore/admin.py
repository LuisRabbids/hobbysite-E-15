from django.contrib import admin
from .models import ProductType, Product, Transaction

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description'
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'product_type',
        'owner',
        'price',
        'stock',
        'status'
    )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'buyer',
        'amount',
        'status',
        'created_on'
    )