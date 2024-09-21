from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, DetailView, View
from category.models import Category
from .models import Product
from cart.models import CartItem
from cart.views import _cart_id
from rest_framework import viewsets
from .serializers import ProductSerializer


# region show products

class ProductsPageView(ListView):
    model = Product
    paginate_by = 2
    template_name = 'store/products_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            queryset = Product.objects.filter(available=True, category=category).order_by('id')
        else:
            queryset = Product.objects.filter(available=True).order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_count'] = self.get_queryset().count()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()  # Get the current product

        # Get cart items associated with this product
        cart_items = CartItem.objects.filter(product=product)
        context['cart_items'] = cart_items

        # Check if the product exists in the user's cart
        try:
            cart_item = CartItem.objects.filter(product=product, cart__cart_id=_cart_id(self.request))
            context['cart_exist'] = True
        except CartItem.DoesNotExist:
            context['cart_exist'] = False

        return context


# endregion


# region search

class SearchClassBaseView(View):
    paginate_by = 2  # Set the number of items per page globally for the class

    def get(self, request):
        # Get the product list and the search query
        products = Product.objects.all().order_by('id')
        query = request.GET.get('keyword')  # GET method should use request.GET, not request.POST

        if query:
            # Filter products by query if it exists
            products = Product.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(name__icontains=query)
            )

        # Paginate the product list
        paginator = Paginator(products, self.paginate_by)  # Paginate by the number of items set

        page = request.GET.get('page')  # Get the page number from the request

        try:
            products_paginated = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, show the first page
            products_paginated = paginator.page(2)
        except EmptyPage:
            # If page is out of range, show the last page of results
            products_paginated = paginator.page(paginator.num_pages)

        # Render the template with the paginated products
        return render(request, 'search_result.html', {'products': products_paginated})

    def post(self, request):
        # Similar logic as the GET request
        products = Product.objects.all().order_by('id')
        query = request.POST.get('keyword')
        count = 0

        if query:
            # Filter products by query if it exists
            products = Product.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(name__icontains=query)
            )
            count = products.count()

        # Paginate the product list
        paginator = Paginator(products, self.paginate_by)  # Paginate by 1 item per page
        page = request.GET.get('page')  # Get the page number from the request

        try:
            products_paginated = paginator.page(page)
        except PageNotAnInteger:
            products_paginated = paginator.page(1)
        except EmptyPage:
            products_paginated = paginator.page(paginator.num_pages)

        # Render the template with the paginated products
        return render(request, 'search_result.html', {'products': products_paginated, 'count': count})


# endregion


# region Api

class ProductvViewsets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    paginate_by = 2
    serializer_class = ProductSerializer

# endregion
