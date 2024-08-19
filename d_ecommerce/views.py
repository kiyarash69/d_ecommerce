from django.shortcuts import render
from store.models import Product

def home(request):
    products = Product.objects.all().filter(available=True)
    return render(request, 'home.html', {'product' : products} )
