from django.shortcuts import render, redirect
from . import models, forms
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse

# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = forms.OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                models.OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect
            return redirect(reverse('payment:process'))
    else:
        form = forms.OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
