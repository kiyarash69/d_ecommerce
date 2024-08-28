from django.db import models
from store.models import Product, Variation


class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    created = models.DateField('created at', auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitem')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitem')
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name
