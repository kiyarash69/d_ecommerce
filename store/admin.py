from django.contrib import admin

from category.models import Category
from .models import Product, Variation, ReviewRating


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'stock', 'available', 'created']
    readonly_fields = ['created', 'modified']


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active']
    list_filter = ('product', 'variation_category', 'is_active',)
    list_editable = ('is_active',)


@admin.register(ReviewRating)
class RewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'status', 'ip', 'created_at']
