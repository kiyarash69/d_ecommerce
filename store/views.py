from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, DetailView, View
from category.models import Category
from .models import Product
from cart.models import CartItem
from cart.views import _cart_id


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
            cart_item = CartItem.objects.get(product=product, cart__cart_id=_cart_id(self.request))
            context['cart_exist'] = True
        except CartItem.DoesNotExist:
            context['cart_exist'] = False

        return context


class SearchClassBaseView(View):
    def get(self, request):
        products = Product.objects.all().order_by('id')
        query = request.POST.get('keyword')
        if query:
            products = Product.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(name__icontains=query)
            )
        return render(request, 'search_result.html', {'products': products})

    def post(self, request):
        products = Product.objects.all().order_by('id')
        query = request.POST.get('keyword')
        count = 0
        if query:
            # products = Product.objects.filter(
            #     Q(title__icontains=query) | Q(description__icontains=query) | Q(name__icontains=query)
            # )
            products = Product.objects.filter(
                Q(title__search=query) | Q(description__search=query) | Q(name__search=query)
            )
            count = products.count()

        return render(request, 'search_result.html', {"products": products , 'count' : count})
