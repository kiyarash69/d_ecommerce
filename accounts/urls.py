from django.urls import path
from . import views

app_name = 'account_app'
urlpatterns = [
    path('register', views.RegisterClassBaseView.as_view(), name='register'),

]
