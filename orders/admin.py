from django.contrib import admin
from . import models


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_method', 'amount_paid', 'created_at', 'payment_method', 'status']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered',
                    'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]


@admin.register(models.OrderProduct)
class ProductOrder(admin.ModelAdmin):
    list_display = [
        'user', 'quantity', 'created_at',
    ]
