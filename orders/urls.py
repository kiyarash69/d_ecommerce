from django.urls import path
from . import views

app_name = 'order_app'
urlpatterns = [
    path('place_order/', views.PlaceOrderView.as_view(), name='place_order'),
    path('payment/', views.payments, name='payment'),
    path('complete', views.order_complete, name='order_complete'),
]
