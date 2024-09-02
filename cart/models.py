from django.db import models
from store.models import Product, Variation
import uuid


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, unique=True, blank=True)
    created = models.DateField('created at', auto_now_add=True)

    def __str__(self):
        return self.cart_id

    def save(self, *args, **kwargs):
        if not self.cart_id:
            self.cart_id = str(uuid.uuid4())  # Generate unique cart_id
        super().save(*args, **kwargs)


class CartItem(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitem')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitem')
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


