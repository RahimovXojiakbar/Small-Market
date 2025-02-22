from django.contrib import admin
from . import models
from unfold.admin import ModelAdmin





@admin.register(models.Brand)
class BrandAdmin(ModelAdmin):
    list_display = ['uuid', 'name']
    search_fields = ['name']


@admin.register(models.Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['uuid', 'name']
    search_fields = ['name']



@admin.register(models.CustomerProfile)
class CustomerProfileAdmin(ModelAdmin):
    list_display = ['uuid', 'user', 'phone_number']
    search_fields = ['user']



@admin.register(models.Order)
class OrderAdmin(ModelAdmin):
    list_display = ['uuid', 'customer', 'order_status']
    search_fields = ['customer']
    list_filter = ['order_status' ,'customer']


@admin.register(models.OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['uuid', 'order' ,'product_variant' ,'price']
    search_fields = ['order']
    list_filter = ['order', 'product_variant']


@admin.register(models.ProductBase)
class PrductBaseAdmin(ModelAdmin):
    list_display = ['uuid', 'name', 'category']
    search_fields = ['name']
    list_filter = ['category', 'brand', 'is_featured']




@admin.register(models.ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = ['uuid', 'product_base', 'name', 'price', 'stock_quantity']
    search_fields = ['name']
    list_filter = ['product_base']


