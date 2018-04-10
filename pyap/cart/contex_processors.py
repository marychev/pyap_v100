from cart.cart import Cart


def cart(request):
    """Общие данные для корзины (для все страниц)"""
    return {'cart': Cart(request)}

