from django.urls import path
from . import views

app_name = 'cart_app'
urlpatterns = [
    path('', views.ProductCartView.as_view(), name='product_cart'),
    path('add/<int:product_id>/', views.AddCartView.as_view(), name='add_to_cart') ,
    path('product/decrease/<str:unique_id>/', views.decrease_added_product, name='product_decrease') ,
    path('product/Remove/<str:unique_id>/', views.remove_cart_view, name='product_remove') ,

]
