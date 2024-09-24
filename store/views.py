from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import ListView, DetailView, View
from category.models import Category
from orders.models import OrderProduct
from .forms import ReviewForm
from .models import Product, ReviewRating
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
        context['cart_exist'] = CartItem.objects.filter(product=product, cart__cart_id=_cart_id(self.request)).exists()

        if self.request.user.is_authenticated:
            order_product = OrderProduct.objects.filter(user=self.request.user, product_id=product.id).exists()
        else:
            order_product = None

        context['reviews'] = ReviewRating.objects.filter(product_id=product.id, status=True)

        context['order_product'] = order_product
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

# region submit review


class ReviewSumitView(View):
    def post(self, request, product_id):
        url = request.META.get('HTTP_REFERER')
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

# endregion
