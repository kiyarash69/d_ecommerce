from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', viewset=views.ProductvViewsets)

app_name = 'store_app'
urlpatterns = [
    path('all/', views.ProductsPageView.as_view(), name='products_page'),
    path('search/', views.SearchClassBaseView.as_view(), name='search'),
    path('category/<slug:slug>/', views.ProductsPageView.as_view(), name='products_by_category'),
    path('detail/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('viewset/products', include(router.urls), name='view_set'),
    path('review/submit/<int:product_id>/', views.ReviewSumitView.as_view(), name='review_submit')
]
