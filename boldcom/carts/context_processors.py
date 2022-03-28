from .models import Cart, CartItem
from . views  import _cart_id







# ========>  this function will count inside the cart icon    <========

def counter(request):
    # ===> if we are inside the admin we dont want to see anything
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            # ===> this '_cart_id(request)' contains the session keys
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            # ===> we are bringing the corresponding cart items
            cart_items = CartItem.objects.all().filter(cart = cart[:1])
            # ===> we are getting the cart item quantity
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        # ===> if the cart does not exist
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count = cart_count)