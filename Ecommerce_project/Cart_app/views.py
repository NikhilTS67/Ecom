from django.shortcuts import render, redirect, get_object_or_404
from Ecommerce_app.models import Product
from .models import Cart, CartItems
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def cart_ID(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.stock >= 1:
        try:
            cart = Cart.objects.get(cart_id=cart_ID(request))
            product.stock -= 1
            product.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=cart_ID(request))
            cart.save()
        try:
            cart_item = CartItems.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItems.DoesNotExist:
            cart_item = CartItems.objects.create(product=product, cart=cart, quantity=1)
        return redirect('cart:cart_details')
    else:
        return redirect('/')


def cart_details(request, total=0, counter=0, cart_items=None):
    try:

        cart = Cart.objects.get(cart_id=cart_ID(request))
        cart_items=CartItems.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=cart_ID(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItems.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        product.stock += 1
        cart_item.save()
        product.save()
    else:
        cart_item.delete()
        product.stock += 1
        product.save()
    return redirect('cart:cart_details')


def delete_cart(request, product_id):
    cart = Cart.objects.get(cart_id=cart_ID(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItems.objects.get(product=product, cart=cart)
    product.stock += cart_item.quantity
    product.save()
    cart_item.delete()
    return redirect('cart:cart_details')

