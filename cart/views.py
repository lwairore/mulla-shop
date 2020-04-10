from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop import models as shop_models
from . import cart
from . import forms

# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = cart.Cart(request)
    product = get_object_or_404(shop_models.Product, id=product_id)
    form = forms.CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')
