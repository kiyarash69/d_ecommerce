from django.contrib import admin
from django.urls import path, include  # Correct import statements
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
                  path('درگاه_امن/', admin.site.urls),
                  path('', views.home, name='home'),  # Root URL mapped to home view
                  path('product/', include('store.urls')),  # Including store.urls for product
                  path('cart/', include('cart.urls')),  # Including cart.urls for cart
                  path('account/', include('accounts.urls')),  # Including account.urls for register and login etc .
                  path('order/', include('orders.urls')),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serving media files
