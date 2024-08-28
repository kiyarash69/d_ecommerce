from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


class ProductCartView(View):
    def get(self, request, total=0, quantity=0, cart_item=None):
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for item in cart_items:
                total += (item.product.price * item.quantity)
                quantity += item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass

        context = {
            "total": total,
            "quantity": quantity,
            "items": cart_items,
            "tax": tax,
            "grand_total": grand_total
        }
        return render(request, 'store/cart.html', context)


# region defs

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def decrease_added_product(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    select = CartItem.objects.get(product=product, cart=cart)
    if select.quantity <= 1:
        select.delete()
    else:
        select.quantity -= 1
        select.save()
    return redirect('cart_app:product_cart')


def RemoveCartView(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    select = CartItem.objects.get(product=product, cart=cart)
    select.delete()
    return redirect('cart_app:product_cart')


# endregion


class AddCartView(View):
    def get(self, request, product_id):
        product_h = Product.objects.get(id=product_id)  # get the product

        try:
            cart_h = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart_h = Cart.objects.create(cart_id=_cart_id(request))

        cart_h.save()

        try:
            cart_item = CartItem.objects.get(product=product_h, cart=cart_h)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product_h,
                quantity=1,
                cart=cart_h,
            )
            cart_item.save()

        return redirect('cart_app:product_cart')

    def post(self, request, product_id):
        product_h = Product.objects.get(id=product_id)  # get the product
        products_variation_list = []
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product_h, variation_category__iexact=key,
                                                  variation_value__iexact=value)
                products_variation_list.append(variation)

                print(products_variation_list)
            except:
                pass
            return redirect('cart_app:product_cart')
