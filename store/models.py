from django.db import models
from category.models import Category
from decimal import Decimal, ROUND_HALF_UP


class Product(models.Model):
    """
    Represents a product in the inventory, including details such as name,
    description, price, stock, and category.
    """
    name = models.CharField(max_length=30, verbose_name="Product Name")
    title = models.CharField(max_length=70, verbose_name="Product Title")
    slug = models.SlugField(verbose_name="Product Slug")
    description = models.TextField('Long Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product Price")
    discount = models.IntegerField('Product Discount', blank=True, null=True)
    image = models.ImageField(upload_to='photos/product', verbose_name="Product Image")
    stock = models.PositiveIntegerField('Remaining in Stock')
    available = models.BooleanField('Is Available in Stock', default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Product Category")
    created = models.DateTimeField('Created at', auto_now_add=True)
    modified = models.DateTimeField('Modified at', auto_now=True)

    def __str__(self):
        return self.name


    def get_discounted_price(self):
        # Ensure the discount is not None and is a valid percentage
        if self.discount is not None:
            # Convert discount percentage to Decimal and calculate discount factor
            discount_percent = Decimal(self.discount) / Decimal(100)
            discount_factor = Decimal(1) - discount_percent

            # Calculate discounted price
            discounted_price = self.price * discount_factor

            # Debug: Print values to verify calculations
            print(f"Original Price: {self.price}")
            print(f"Discount Percent: {discount_percent}")
            print(f"Discount Factor: {discount_factor}")
            print(f"Discounted Price: {discounted_price}")

            # Return the discounted price rounded to 2 decimal places
            return discounted_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # If no discount, return the original price
        return self.price
