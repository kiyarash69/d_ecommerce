from django.shortcuts import render
from store.models import Product
from store.models import ReviewRating


def home(request):
    products = Product.objects.filter(available=True)

    product_reviews = {}

    for product in products:
        reviews = ReviewRating.objects.filter(product=product.id, status=True)
        product_reviews[product.id] = reviews

    context = {'products': products, 'product_reviews': product_reviews}

    return render(request, 'home.html', context)
