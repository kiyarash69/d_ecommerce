from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView , DetailView
from category.models import Category
from .models import Product


class ProductsPageView(ListView):
    model = Product
    template_name = 'store/products_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            queryset = Product.objects.filter(available=True, category=category)
        else:
            queryset = Product.objects.filter(available=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_count'] = self.get_queryset().count()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs['slug'])
