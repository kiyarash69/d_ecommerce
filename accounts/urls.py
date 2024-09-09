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
]
