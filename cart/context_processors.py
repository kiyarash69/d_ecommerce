from .models import Cart , CartItem
from .views import _cart_id


def conter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else :
        try:
            cart_items = CartItem.objects.all()
            for cart_item in cart_items :
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_item = 0

    return dict(cart_count=cart_count)
