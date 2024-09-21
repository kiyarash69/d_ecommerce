from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from orders.models import Order
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin


# region Cart view

class ProductCartView(View):
    def get(self, request, total=0, quantity=0, cart_items=None):
        tax = 0
        grand_total = 0
        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
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
        current_user = request.user
        product = Product.objects.get(id=product_id)  # Get the product

        # Retrieve product variations from request
        product_variation = []
        for item in request.GET:
            key = item
            value = request.GET[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

        # If the user is authenticated
        if current_user.is_authenticated:
            return self.handle_cart_for_authenticated_user(request, product, product_variation, current_user)
        else:
            return self.handle_cart_for_unauthenticated_user(request, product, product_variation)

    def handle_cart_for_authenticated_user(self, request, product, product_variation, user):
        cart_items = CartItem.objects.filter(product=product, user=user)

        if cart_items.exists():
            return self.update_or_create_cart_item(cart_items, product_variation, product, user=user)
        else:
            return self.create_cart_item(product, product_variation, user=user)

    def handle_cart_for_unauthenticated_user(self, request, product, product_variation):
        cart_id = _cart_id(request)
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
        cart_items = CartItem.objects.filter(product=product, cart=cart)

        if cart_items.exists():
            return self.update_or_create_cart_item(cart_items, product_variation, product, cart=cart)
        else:
            return self.create_cart_item(product, product_variation, cart=cart)

    def update_or_create_cart_item(self, cart_items, product_variation, product, user=None, cart=None):
        ex_var_list = []
        id_list = []

        # Prepare existing variations and their cart item IDs
        for item in cart_items:
            existing_variations = list(item.variations.all())
            ex_var_list.append(existing_variations)
            id_list.append(item.id)

        if product_variation in ex_var_list:
            # If variations match, increase quantity
            index = ex_var_list.index(product_variation)
            item_id = id_list[index]
            item = CartItem.objects.get(id=item_id)
            item.quantity += 1
            item.save()
        else:
            # Create a new cart item if variations don't match
            item = CartItem.objects.create(product=product, quantity=1, user=user, cart=cart)
            if product_variation:
                item.variations.add(*product_variation)
            item.save()

        return redirect('cart_app:product_cart')

    def create_cart_item(self, product, product_variation, user=None, cart=None):
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=user,
            cart=cart,
        )
        if product_variation:
            cart_item.variations.add(*product_variation)
        cart_item.save()

        return redirect('cart_app:product_cart')

    def remove_cart(request, product_id, cart_item_id):

        product = get_object_or_404(Product, id=product_id)
        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except:
            pass
        return redirect('cart_app:product_cart')


# endregion


# region Checkout


class CheckoutView(LoginRequiredMixin, View):
    login_url = 'account_app:login'

    def get(self, request, total=0, quantity=0, cart_items=None):
        try:
            tax = 0
            grand_total = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)

            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity

            tax = (2 * total) / 100
            grand_total = total + tax

        except ObjectDoesNotExist:
            # Handle the case where the cart or cart items do not exist
            cart_items = []

        context = {
            "total": total,
            "quantity": quantity,
            "cart_items": cart_items,
            "tax": tax,
            "grand_total": grand_total
        }

        return render(request, 'store/checkout.html', context)

# end region
