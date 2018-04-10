from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from generic.mixins import MainPageMixin
from cart.cart import Cart
from product.models import ProductItem
from .models import OrderItem
from .froms import OrderCreateForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class OrderCreate(MainPageMixin, TemplateView):
    """
    Страница оформление заказа
    """
    template_name = 'order/templates/create.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['cart'] = Cart(context['request'])
        context['form'] = OrderCreateForm(
            initial={'cart': context['cart'], 'user': context['request'].user})
        context['breadcrumbs'] = [
            {'title': 'Корзина', 'url': '/cart/'},
            {'title': 'Оформление заказа', 'url': '/order/create/'}
        ]
        context['order'] = None
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        cart = Cart(request)
        form = OrderCreateForm(
            request.POST, initial={
                'cart': cart, 'user': context['request'].user})

        if form.is_valid():
            context['order'] = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=context['order'], product_item=item['product'],
                    price=item['price'], quantity=item['quantity'])

                # вычесть из общего кол-ва варианта товара
                product_item = ProductItem.objects.get(id=item['product'].id)
                product_item.quantity -= item['quantity']
                product_item.save()

            cart.clear()
            return redirect('/order/' + str(context['order'].pk) + '/created/')
        return render(request, self.template_name, context=context)


class OrderCreated(MainPageMixin, TemplateView):
    """
    Страница успешного оформления зкаказа и перехода к нему
    """
    template_name = 'order/templates/created.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCreated, self).get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'title': 'Корзина', 'url': '/cart/'},
            {'title': 'Заказ {}'.format(context['pk']), 
                'url': 'users/{}/order'.format(context['pk'])}
        ]
        return context


