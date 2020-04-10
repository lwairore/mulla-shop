from . import cart


def cart(request):
    return {'cart': cart.Cart(request)}
