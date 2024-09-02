from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


# region Cart view

class ProductCartView(View):
    def get(self, request, total=0, quantity=0, cart_items=None):
        tax = 0
        grand_total = 0
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for item in cart_items:
                total += (item.product.price * item.quantity)
                quantity += item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
        except ObjectDoesNotExist:
            cart_items = []

        context = {
            "total": total,
            "quantity": quantity,
            "items": cart_items,
            "tax": tax,
            "grand_total": grand_total
        }
        return render(request, 'store/cart.html', context)


# endregion


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# region decrease and remove cart item

def decrease_added_product(request, unique_id):
    try:
        # Get the single cart item object instead of a QuerySet
        cart_item = CartItem.objects.get(unique_id=unique_id)
        if cart_item.quantity <= 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart_app:product_cart')


def remove_cart_view(request, unique_id):
    try:
        cart_item = CartItem.objects.get(unique_id=unique_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart_app:product_cart')


# endregion


# region  Cart logic

class AddCartView(View):
    def get(self, request, product_id):
        try:
            product_h = Product.objects.get(id=product_id)  # Get the product
        except Product.DoesNotExist:
            return HttpResponse('Page Not Found')

        # Start variation code
        products_variation_list = []
        for item in request.GET:
            key = item
            value = request.GET[key]
            try:
                variation = Variation.objects.get(
                    product=product_h,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                products_variation_list.append(variation)
            except Variation.DoesNotExist:
                pass
        # End variation code

        # Get the cart object or create one if it doesn't exist
        try:
            cart_h = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart_h = Cart.objects.create(cart_id=_cart_id(request))

        cart_h.save()

        # Get all cart items with the same product and cart
        cart_items = CartItem.objects.filter(product=product_h, cart=cart_h)

        # Check for exact match of variations in existing cart items
        for item in cart_items:
            existing_variations = list(item.variations.all())
            if existing_variations == products_variation_list:
                # If variations match, increase quantity
                item.quantity += 1
                item.save()
                return redirect('cart_app:product_cart')

        # If no matching variations found, create a new cart item
        cart_item = CartItem.objects.create(
            product=product_h,
            quantity=1,
            cart=cart_h
        )
        if len(products_variation_list) > 0:
            cart_item.variations.add(*products_variation_list)
        cart_item.save()

        return redirect('cart_app:product_cart')

# endregion
