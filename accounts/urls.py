from django.urls import path
from . import views

app_name = 'account_app'
urlpatterns = [
    path('register/', views.RegisterClassBaseView.as_view(), name='register'),
    path('login/', views.LoginClassBaseView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('dashboard/', views.DashboardClassBaseView.as_view(), name='dashboard'),
    path('', views.DashboardClassBaseView.as_view(), name='dashboard'),
    path('forgot/password/', views.ForgotPasswordClassBaseView.as_view(), name='forgot_p'),
    path('reset/password/validate/<uidb64>/<token>/', views.ResetPasswordValidate.as_view(),
         name='reset_password_validate'),
    path('reset/password', views.ResetPassword.as_view(), name='reset_password'),
    path('my_orders/', views.MyOrdersView.as_view(), name='my_orders'),
    path('edit/profile', views.EditProfileView.as_view(), name='edit_profile'),
    path('change/password', views.ChangePasswordView.as_view(), name='change_password'),
    path('my/orders/detail/<int:order_number>/', views.MyOrdersDetail.as_view(), name='my_orders_detail'),
]
