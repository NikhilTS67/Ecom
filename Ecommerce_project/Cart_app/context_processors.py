from .models import Cart, CartItems
from .views import cart_ID


def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=cart_ID(request))
            cart_items = CartItems.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoseNotExist:
            item_count = 0
    return dict(item_count=item_count)