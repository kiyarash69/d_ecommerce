from django.urls import path
from . import views


app_name = 'store_app'
urlpatterns = [
    path('all/', views.ProductsPageView.as_view() , name='products_page'),
    path('category/<slug:slug>/', views.ProductsPageView.as_view(), name='products_by_category'),
    path('detail/<slug:slug>' , views.ProductDetailView.as_view() , name = 'product_detail' ) ,
]
