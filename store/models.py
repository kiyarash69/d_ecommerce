from django.db import models

from accounts.models import Account
from category.models import Category
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Avg, Count


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

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

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

            # Return the discounted price rounded to 2 decimal places
            return discounted_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # If no discount, return the original price
        return self.price


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'Color'),
    ('size', 'Size'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=30, choices=variation_category_choice,
                                          verbose_name="Product Variation Category")
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField('Created at', auto_now_add=True)
    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
