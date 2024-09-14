from .models import Cart , CartItem
from .views import _cart_id


def conter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else :
        try:
            cart = Cart.objects.filter(cart_id=_cart_id)
            print(cart)
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
                print(cart_items)
            else :
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
                if cart_items :
                    print(cart_items)
                else :
                    print('none')

            for cart_item in cart_items :
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_item = 0

    return dict(cart_count=cart_count)
